from __future__ import annotations

import logging
from datetime import datetime, timedelta

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.util import dt as dt_util
from homeassistant.helpers.event import async_track_time_change
from homeassistant.helpers.entity import EntityCategory  # <-- added

_LOGGER = logging.getLogger(__name__)

DOMAIN = "wtime"


def _now_local() -> datetime:
    """Return HA's current local time (aware)."""
    return dt_util.now()


def _is_dst(ts: datetime) -> bool:
    """Return True if DST is in effect at the given aware datetime."""
    off = ts.dst()
    return off is not None and off != timedelta(0)


def _offset(ts: datetime) -> timedelta:
    """UTC offset including DST at ts."""
    return ts.utcoffset() or timedelta(0)


def _find_transition_forward(start: datetime, max_days: int = 400) -> datetime | None:
    """
    Find the next instant the UTC offset changes (DST boundary) after `start`.

    Strategy:
      1) Step by day until offset changes.
      2) Binary-ish refine by hours, then minutes, then seconds to get the exact minute.
    """
    tz = dt_util.DEFAULT_TIME_ZONE
    start = start.astimezone(tz)
    base_off = _offset(start)

    # 1) Coarse day scan
    day_cursor = start
    for _ in range(max_days):
        day_cursor += timedelta(days=1)
        if _offset(day_cursor) != base_off:
            break
    else:
        return None  # no change within window

    # 2) Refine back to the change within that day
    low = day_cursor - timedelta(days=1)
    high = day_cursor

    # Hour refine
    for _ in range(24):
        mid = low + (high - low) / 2
        if _offset(mid) == base_off:
            low = mid
        else:
            high = mid
        if (high - low) <= timedelta(hours=1):
            break

    # Minute refine
    while (high - low) > timedelta(minutes=1):
        mid = low + (high - low) / 2
        if _offset(mid) == base_off:
            low = mid
        else:
            high = mid

    # Second refine (optional: makes the minute accurate even on odd transitions)
    while (high - low) > timedelta(seconds=1):
        mid = low + (high - low) / 2
        if _offset(mid) == base_off:
            low = mid
        else:
            high = mid

    # Return the first minute at/after the change
    change = high.replace(microsecond=0)
    # normalize to minute boundary
    if change.second != 0:
        change = (change + timedelta(minutes=1)).replace(second=0, microsecond=0)
    return change


def _find_transition_backward(start: datetime, max_days: int = 400) -> datetime | None:
    """Find the most recent instant the UTC offset changed before `start`."""
    tz = dt_util.DEFAULT_TIME_ZONE
    start = start.astimezone(tz)
    base_off = _offset(start)

    # Coarse day scan backwards
    day_cursor = start
    for _ in range(max_days):
        day_cursor -= timedelta(days=1)
        if _offset(day_cursor) != base_off:
            break
    else:
        return None

    # Refine forward within that day to the change
    low = day_cursor
    high = day_cursor + timedelta(days=1)

    # We know somewhere in (low, high) the offset equals base_off (after crossing)
    # Narrow until we cross to base_off.
    while (high - low) > timedelta(hours=1):
        mid = low + (high - low) / 2
        if _offset(mid) == base_off:
            high = mid
        else:
            low = mid

    while (high - low) > timedelta(minutes=1):
        mid = low + (high - low) / 2
        if _offset(mid) == base_off:
            high = mid
        else:
            low = mid

    while (high - low) > timedelta(seconds=1):
        mid = low + (high - low) / 2
        if _offset(mid) == base_off:
            high = mid
        else:
            low = mid

    change = low.replace(microsecond=0)
    if change.second != 0:
        change = (change + timedelta(minutes=1)).replace(second=0, microsecond=0)
    return change


class WTimeDSTBinarySensor(BinarySensorEntity):
    """DST status sensor with transition attributes."""

    _attr_name = "WTime DST Status"
    _attr_entity_category = EntityCategory.DIAGNOSTIC  # <-- added
    _attr_should_poll = False  # <-- added

    def __init__(self, entry_id: str) -> None:
        self._attr_unique_id = f"{entry_id}_dst_active"
        self._attr_is_on = False
        self._attrs: dict[str, str | bool | None] = {}
        self._unsub_time = None
        self._entry_id = entry_id  # for device attachment

    @property
    def extra_state_attributes(self) -> dict:
        return self._attrs

    @property
    def device_info(self) -> dict:
        """Attach to the WTime device so it shows under the integration and inherits Area."""
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": "WTime",
            "manufacturer": "AutoH Cloud",
            "model": "WTime Virtual",
        }

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        # Update immediately, then on a schedule
        self._recalc_and_write()

        # Recalculate every 5 minutes to keep next_* fresh without spamming
        self._unsub_time = async_track_time_change(
            self.hass, self._handle_time_tick, second=0, minute=range(0, 60, 5)
        )

    async def async_will_remove_from_hass(self) -> None:
        if self._unsub_time:
            self._unsub_time()
            self._unsub_time = None
        await super().async_will_remove_from_hass()

    @callback
    def _handle_time_tick(self, *_) -> None:
        self._recalc_and_write()

    def _serialize_dt(self, ts: datetime | None) -> str | None:
        if ts is None:
            return None
        # Return local ISO (e.g., 2025-11-02T01:59:00-04:00)
        return ts.astimezone(dt_util.DEFAULT_TIME_ZONE).isoformat(timespec="minutes")

    def _recalc_and_write(self) -> None:
        now = _now_local()
        tz = dt_util.DEFAULT_TIME_ZONE
        now = now.astimezone(tz)

        is_dst_now = _is_dst(now)
        self._attr_is_on = is_dst_now

        # Find prev & next transitions around 'now'
        prev_change = _find_transition_backward(now)
        next_change = _find_transition_forward(now)

        # Determine which side of the boundary is DST
        # For next change, check state just AFTER it
        def _state_after(ts: datetime | None) -> bool | None:
            if ts is None:
                return None
            return _is_dst(ts + timedelta(minutes=1))

        def _state_before(ts: datetime | None) -> bool | None:
            if ts is None:
                return None
            return _is_dst(ts - timedelta(minutes=1))

        next_is_dst = _state_after(next_change)
        prev_is_dst = _state_before(prev_change)

        # Figure season markers + explicit next_start/next_end
        season_start = None  # when DST turned on for the current/most recent season
        season_end = None    # when DST will turn off for the current season (if in DST)

        next_start = None
        next_end = None

        if is_dst_now:
            # We are in DST: previous change must have been "start", next change is "end"
            if prev_change is not None and prev_is_dst is False:
                season_start = prev_change
            else:
                # fallback: find previous "on" change
                season_start = prev_change

            season_end = next_change
            next_start = _find_transition_forward(season_end + timedelta(minutes=1)) if season_end else None
            if next_start is not None:
                # the next end is the following transition after next_start
                next_end = _find_transition_forward(next_start + timedelta(minutes=1))
        else:
            # We are in Standard Time: next change should be "start"
            next_start = next_change if next_is_dst else None
            # The next end is the change after the start
            if next_start is not None:
                next_end = _find_transition_forward(next_start + timedelta(minutes=1))

            # season_end (for the *last* season) was the previous change if it went off
            if prev_change is not None and prev_is_dst is True:
                # previous change turned DST off -> this is last season_end
                season_end = prev_change
                # and to be nice, also compute the last season_start (prev before that)
                last_start = _find_transition_backward(season_end - timedelta(minutes=1))
                if last_start is not None:
                    season_start = last_start

        self._attrs = {
            "dst_in_effect": is_dst_now,
            "timezone": str(tz),
            "season_start": self._serialize_dt(season_start),  # when DST turned on most recently
            "season_end": self._serialize_dt(season_end),      # when DST will turn off (if in DST) or last time it ended
            "next_start": self._serialize_dt(next_start),      # next time DST will start
            "next_end": self._serialize_dt(next_end),          # next time DST will end
            "next_change": self._serialize_dt(next_change),    # immediate next offset flip of any kind
            "next_state": ("on" if (next_is_dst is True) else ("off" if next_is_dst is False else None)),
        }

        _LOGGER.debug("DST attrs recalculated: %s", self._attrs)
        self.async_write_ha_state()


class WTimeWeekdayBinarySensor(BinarySensorEntity):
    """Simple weekday sensor (Mon–Fri)."""

    _attr_name = "WTime Is Weekday"
    _attr_entity_category = EntityCategory.DIAGNOSTIC  # <-- added
    _attr_should_poll = False  # <-- added

    def __init__(self, entry_id: str) -> None:
        self._attr_unique_id = f"{entry_id}_weekday"
        self._attr_is_on = False
        self._entry_id = entry_id  # for device attachment

    @property
    def device_info(self) -> dict:
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": "WTime",
            "manufacturer": "AutoH Cloud",
            "model": "WTime Virtual",
        }

    async def async_added_to_hass(self) -> None:
        self._update_and_write()
        async_track_time_change(self.hass, self._tick, second=0, minute=0, hour=range(0, 24, 1))

    @callback
    def _tick(self, *_):
        self._update_and_write()

    def _update_and_write(self) -> None:
        now = _now_local()
        self._attr_is_on = now.weekday() < 5
        self.async_write_ha_state()


class WTimeWeekendBinarySensor(BinarySensorEntity):
    """Simple weekend sensor (Sat–Sun)."""

    _attr_name = "WTime Is Weekend"
    _attr_entity_category = EntityCategory.DIAGNOSTIC  # <-- added
    _attr_should_poll = False  # <-- added

    def __init__(self, entry_id: str) -> None:
        self._attr_unique_id = f"{entry_id}_weekend"
        self._attr_is_on = False
        self._entry_id = entry_id  # for device attachment

    @property
    def device_info(self) -> dict:
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": "WTime",
            "manufacturer": "AutoH Cloud",
            "model": "WTime Virtual",
        }

    async def async_added_to_hass(self) -> None:
        self._update_and_write()
        async_track_time_change(self.hass, self._tick, second=0, minute=0, hour=range(0, 24, 1))

    @callback
    def _tick(self, *_):
        self._update_and_write()

    def _update_and_write(self) -> None:
        now = _now_local()
        self._attr_is_on = now.weekday() >= 5
        self.async_write_ha_state()


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up the WTime binary sensors."""
    _LOGGER.debug(
        "Setting up WTimeBinarySensors with HA timezone: %s",
        hass.config.time_zone or "UTC",
    )

    async_add_entities(
        [
            WTimeDSTBinarySensor(entry.entry_id),
            WTimeWeekdayBinarySensor(entry.entry_id),
            WTimeWeekendBinarySensor(entry.entry_id),
        ]
    )
