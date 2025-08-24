"""
WTime sensors
- Diagnostic entities
- Only 24-hour clocks are disabled-by-default
- Minute clocks aligned to minute boundary to avoid ~1 min drift
- ENUM options for weekday/month/season/day_of_month
- Pretty date (long + short) with both variants in attributes
- Month number exposes rich attributes
- Season sensor exposes next-change timing + countdown
"""

from __future__ import annotations

from datetime import datetime, timedelta, date
from typing import Any, Dict, Optional, List, Tuple

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.event import (
    async_track_time_interval,
    async_call_later,
)
from homeassistant.helpers.entity import EntityCategory

# Safe import for ENUM device class across HA versions
try:
    from homeassistant.components.sensor import SensorDeviceClass  # HA 2023.9+
except Exception:  # pragma: no cover
    SensorDeviceClass = None  # Fallback

DOMAIN = "wtime"

# ---------- Static label sets ----------
MONTHS: List[str] = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]
SEASONS: List[str] = ["Winter", "Spring", "Summer", "Fall"]
WEEKDAYS: List[str] = [
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday",
]
DAYS_1_TO_31: List[str] = [str(i) for i in range(1, 32)]


# ---------- Helpers ----------
def _guess_season(month: int) -> str:
    """Simple northern-hemisphere season by month."""
    if month in (12, 1, 2):
        return "Winter"
    if month in (3, 4, 5):
        return "Spring"
    if month in (6, 7, 8):
        return "Summer"
    return "Fall"


def _season_bounds_for_year(yr: int) -> Dict[str, Tuple[date, date]]:
    """Return (start,end) dates (inclusive start, exclusive end) for seasons in a given year."""
    # Using meteorological seasons:
    # Winter = Dec 1 (prev year) -> Mar 1, Spring = Mar 1 -> Jun 1, Summer = Jun 1 -> Sep 1, Fall = Sep 1 -> Dec 1
    return {
        "Winter": (date(yr - 1, 12, 1), date(yr, 3, 1)),
        "Spring": (date(yr, 3, 1), date(yr, 6, 1)),
        "Summer": (date(yr, 6, 1), date(yr, 9, 1)),
        "Fall":   (date(yr, 9, 1), date(yr, 12, 1)),
    }


def _current_season_and_next_bounds(today: date) -> Tuple[str, Tuple[date, date], str, Tuple[date, date]]:
    """Given a date, return (season, (start, end), next_season, (next_start, next_end))."""
    seasons = _season_bounds_for_year(today.year)
    for name in ("Winter", "Spring", "Summer", "Fall"):
        start, end = seasons[name]
        # Winter may start last year; adjust map for Dec
        if name == "Winter" and today >= date(today.year, 12, 1):
            # For Dec, winter is current year's Winter starting today.year, 12, 1 -> next year Mar 1
            start, end = (date(today.year, 12, 1), date(today.year + 1, 3, 1))

        if start <= today < end:
            # determine next season in order
            idx = SEASONS.index(name)
            next_name = SEASONS[(idx + 1) % 4]
            # Next season bounds could be in next year
            if next_name == "Winter":
                next_bounds = _season_bounds_for_year(end.year + (1 if end.month == 12 else 0))["Winter"]
                # For our convention above, Winter after Fall starts 12/1 of end.year
                next_bounds = (date(end.year, 12, 1), date(end.year + 1, 3, 1))
            else:
                nb = _season_bounds_for_year(end.year).get(next_name)
                if next_name == "Spring":
                    nb = (date(end.year, 3, 1), date(end.year, 6, 1))
                elif next_name == "Summer":
                    nb = (date(end.year, 6, 1), date(end.year, 9, 1))
                elif next_name == "Fall":
                    nb = (date(end.year, 9, 1), date(end.year, 12, 1))
                next_bounds = nb
            return name, (start, end), next_name, next_bounds

    # Fallback (shouldn't happen)
    return "Winter", (date(today.year, 12, 1), date(today.year + 1, 3, 1)), "Spring", (date(today.year + 1, 3, 1), date(today.year + 1, 6, 1))


def _humanize_seconds(total: int) -> str:
    """Small humanizer for a duration in seconds."""
    if total < 0:
        total = 0
    days, rem = divmod(total, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, seconds = divmod(rem, 60)
    parts = []
    if days:
        parts.append(f"{days}d")
    if hours:
        parts.append(f"{hours}h")
    if minutes:
        parts.append(f"{minutes}m")
    if seconds and not parts:
        parts.append(f"{seconds}s")
    return " ".join(parts) or "0s"


def _next_minute_delay(now: datetime) -> float:
    """Seconds until next minute boundary."""
    next_minute = (now.replace(second=0, microsecond=0) + timedelta(minutes=1))
    return (next_minute - now).total_seconds()


# ---------- Catalog ----------
#   - format: strftime format string
#   - compute: callable(now) -> value
#   - interval: seconds between updates
#   - enabled_by_default: first-run entity enabled state
#   - options: ENUM options (list[str])
#   - device_class: "enum" when options provided
#   - align: "second" | "minute" | None — first update aligned to boundary (then fixed interval)
SENSORS: Dict[str, Dict[str, Any]] = {
    # Clocks (align minute for minute clocks to avoid drift; seconds clocks tick each second)
    "wtime_12hr_clock": {
        "format": "%-I:%M %p",
        "icon": "mdi:clock-outline",
        "interval": 60,
        "align": "minute",
        "enabled_by_default": True,
    },
    "wtime_24hr_clock": {
        "format": "%H:%M",
        "icon": "mdi:clock-outline",
        "interval": 60,
        "align": "minute",
        "enabled_by_default": False,  # per request
    },
    "wtime_12hr_clock_with_seconds": {
        "format": "%-I:%M:%S %p",
        "icon": "mdi:clock-time-four-outline",
        "interval": 1,
        "align": "second",
        "enabled_by_default": True,
    },
    "wtime_24hr_clock_with_seconds": {
        "format": "%H:%M:%S",
        "icon": "mdi:clock-time-four-outline",
        "interval": 1,
        "align": "second",
        "enabled_by_default": False,  # per request
    },

    # Categorical date parts (ENUM)
    "wtime_weekday": {
        "compute": lambda now: WEEKDAYS[now.weekday()],
        "icon": "mdi:calendar-week",
        "interval": 60,
        "enabled_by_default": True,
        "options": WEEKDAYS,
        "device_class": "enum",
    },
    "wtime_month_name": {
        "compute": lambda now: MONTHS[now.month - 1],
        "icon": "mdi:calendar-month",
        "interval": 3600,
        "enabled_by_default": True,
        "options": MONTHS,
        "device_class": "enum",
    },
    "wtime_season": {
        "compute": lambda now: _guess_season(now.month),
        "icon": "mdi:white-balance-sunny",
        "interval": 3600,
        "enabled_by_default": True,
        "options": SEASONS,
        "device_class": "enum",
    },
    "wtime_day_of_month": {
        "compute": lambda now: str(now.day),
        "icon": "mdi:numeric",
        "interval": 60,
        "enabled_by_default": True,
        "options": DAYS_1_TO_31,
        "device_class": "enum",
    },

    # Numeric/date-ish (no fixed options)
    "wtime_month_number": {
        "compute": lambda now: now.month,
        "icon": "mdi:calendar-month",
        "interval": 3600,
        "enabled_by_default": True,
    },
    "wtime_year": {
        "compute": lambda now: now.year,
        "icon": "mdi:numeric",
        "interval": 3600,
        "enabled_by_default": True,
    },

    # ISO / Pretty (removed datetime ISO per request)
    "wtime_date_iso": {
        "format": "%Y/%m/%d",  # slashes instead of dashes
        "icon": "mdi:calendar",
        "interval": 3600,
        "enabled_by_default": True,
    },
    "wtime_date_pretty": {
        "format": "%A, %B %-d, %Y",
        "icon": "mdi:calendar-star",
        "interval": 3600,
        "enabled_by_default": True,
    },
    "wtime_date_pretty_short": {
        # e.g. "Sun, Aug 24, 2025"
        "format": "%a, %b %-d, %Y",
        "icon": "mdi:calendar-star",
        "interval": 3600,
        "enabled_by_default": True,
    },

    # ISO Week number
    "wtime_iso_week": {
        "compute": lambda now: now.isocalendar()[1],
        "icon": "mdi:counter",
        "interval": 3600,
        "enabled_by_default": True,
    },
}


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
) -> None:
    """Set up WTime sensors from a config entry."""
    entities = [
        WtimeSensor(sensor_key=name, meta=meta, entry_id=entry.entry_id)
        for name, meta in SENSORS.items()
        # NOTE: wtime_datetime_iso intentionally removed
    ]
    async_add_entities(entities, update_before_add=True)


class WtimeSensor(SensorEntity):
    """Representation of a WTime sensor."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, sensor_key: str, meta: Dict[str, Any], entry_id: str) -> None:
        self._key = sensor_key
        self._meta = meta
        self._attr_name = sensor_key.replace("_", " ").title()
        self._attr_unique_id = f"{entry_id}_{sensor_key}"
        self._attr_icon = meta.get("icon")
        self._attr_native_value: Optional[Any] = None

        # Enabled-by-default choice
        self._attr_entity_registry_enabled_default = bool(
            meta.get("enabled_by_default", True)
        )

        # Device class + options for ENUM sensors
        self._attr_options = None
        self._device_class = None
        if meta.get("device_class") == "enum" and SensorDeviceClass is not None:
            self._device_class = SensorDeviceClass.ENUM
            self._attr_options = list(meta.get("options") or [])

        # Update cadence
        self._interval_seconds = int(meta.get("interval", 60))
        self._update_interval = timedelta(seconds=self._interval_seconds)
        self._align = meta.get("align")  # None | "second" | "minute"

        # Timer handle(s)
        self._unsub_timer = None
        self._unsub_once = None  # for first alignment trigger

    # ---- HA properties ----
    @property
    def device_class(self) -> Optional[str]:
        return self._device_class

    @property
    def options(self) -> Optional[List[str]]:
        return self._attr_options

    @property
    def native_value(self) -> Any:
        return self._attr_native_value

    async def async_added_to_hass(self) -> None:
        """Kick off periodic updates with optional boundary alignment."""
        # Immediate compute so UI has value
        self._compute_and_set()

        if self._align == "minute":
            # Wait until the next minute boundary, then start interval ticking
            delay = _next_minute_delay(datetime.now())
            self._unsub_once = async_call_later(self.hass, delay, self._start_interval_after_align)
        elif self._align == "second":
            # Align to next second boundary
            now = datetime.now()
            delay = 1.0 - (now.microsecond / 1_000_000.0)
            if delay <= 0 or delay > 1.0:
                delay = 1.0
            self._unsub_once = async_call_later(self.hass, delay, self._start_interval_after_align)
        else:
            # No alignment; start interval now
            self._unsub_timer = async_track_time_interval(
                self.hass, self._async_timer_tick, self._update_interval
            )

    async def async_will_remove_from_hass(self) -> None:
        """Cleanup."""
        if self._unsub_once:
            self._unsub_once()
            self._unsub_once = None
        if self._unsub_timer:
            self._unsub_timer()
            self._unsub_timer = None

    @callback
    def _start_interval_after_align(self, _now) -> None:
        # First aligned compute to hit the boundary exactly
        self._compute_and_set()
        # Then regular interval ticks
        self._unsub_timer = async_track_time_interval(
            self.hass, self._async_timer_tick, self._update_interval
        )
        # Clear one-shot handle
        if self._unsub_once:
            self._unsub_once()
            self._unsub_once = None

    @callback
    def _async_timer_tick(self, _now) -> None:
        self._compute_and_set()

    def _compute_and_set(self) -> None:
        now = datetime.now()

        # Compute state
        if "compute" in self._meta:
            try:
                value = self._meta["compute"](now)
            except Exception:
                value = None
        elif "format" in self._meta:
            fmt = self._meta["format"]
            try:
                value = now.strftime(fmt)
            except Exception:
                value = now.isoformat(sep=" ", timespec="seconds")
        else:
            value = None

        # Update state if changed
        if value != self._attr_native_value:
            self._attr_native_value = value
            self.async_write_ha_state()
        else:
            # Even if unchanged, attributes may need recalculation (e.g., countdown). Update state anyway.
            self.async_write_ha_state()

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Dynamic attributes per sensor key."""
        attrs: Dict[str, Any] = {}

        now = datetime.now()
        today = now.date()

        # Pretty date sensors: include both long and short in attributes
        if self._key in ("wtime_date_pretty", "wtime_date_pretty_short"):
            pretty_long = now.strftime("%A, %B %-d, %Y")
            pretty_short = now.strftime("%a, %b %-d, %Y")
            attrs["pretty_long"] = pretty_long
            attrs["pretty_short"] = pretty_short

        # Month number rich attributes
        if self._key == "wtime_month_number":
            month_idx = now.month
            # month length (simple, not leap-year aware for February fix below)
            # We'll calculate accurately:
            if month_idx == 12:
                next_month_first = date(now.year + 1, 1, 1)
            else:
                next_month_first = date(now.year, month_idx + 1, 1)
            this_month_first = date(now.year, month_idx, 1)
            month_length = (next_month_first - this_month_first).days

            attrs.update(
                {
                    "name": MONTHS[month_idx - 1],
                    "zero_padded": f"{month_idx:02d}",
                    "month_length": month_length,
                    "first_weekday_name": WEEKDAYS[this_month_first.weekday()],
                }
            )

        # Season: add current end, next season info, and countdown
        if self._key == "wtime_season":
            season, (start, end), next_season, (nstart, nend) = _current_season_and_next_bounds(today)
            # current season changes at `end` 00:00 local
            change_dt = datetime.combine(end, datetime.min.time())
            seconds_left = int((change_dt - now).total_seconds())
            attrs.update(
                {
                    "current_end": end.isoformat(),
                    "next_season": next_season,
                    "next_start": nstart.isoformat(),
                    "next_end": nend.isoformat(),
                    "seconds_until_change": max(0, seconds_left),
                    "countdown_until_change": _humanize_seconds(seconds_left),
                }
            )

        # Day of month ENUM: optionally publish numeric convenience fields
        if self._key == "wtime_day_of_month":
            day = now.day
            attrs.update(
                {
                    "day_int": day,
                    "zero_padded": f"{day:02d}",
                }
            )

        # ISO & Pretty dates: expose yyyy/mm/dd too
        if self._key in ("wtime_date_iso", "wtime_date_pretty", "wtime_date_pretty_short"):
            attrs["y"] = now.year
            attrs["m"] = now.month
            attrs["d"] = now.day
            attrs["iso_with_slashes"] = now.strftime("%Y/%m/%d")

        return attrs
