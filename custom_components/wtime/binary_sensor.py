from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.util import dt as dt_util
from datetime import timedelta
import logging

_LOGGER = logging.getLogger(__name__)

DOMAIN = "wtime"


def _now_local():
    """Return HA's current local time as an aware datetime."""
    # dt_util.now() returns an aware datetime in Home Assistant's configured timezone.
    return dt_util.now()


class WTimeDSTBinarySensor(BinarySensorEntity):
    """Representation of a WTime DST binary sensor."""

    def __init__(self, entry_id: str):
        """Initialize the DST sensor."""
        self._attr_name = "WTime DST Status"
        self._attr_unique_id = f"{entry_id}_dst_active"
        self._attr_is_on = self._check_dst()

    def _check_dst(self) -> bool:
        """Check if Daylight Saving Time (DST) is active."""
        try:
            now = _now_local()
            dst_offset = now.dst()
            _LOGGER.debug("Current local time: %s, DST offset: %s", now, dst_offset)
            return dst_offset is not None and dst_offset != timedelta(0)
        except Exception as err:
            _LOGGER.error("Error checking DST status: %s", err)
            return False

    @property
    def is_on(self) -> bool:
        """Return True if DST is active."""
        return self._attr_is_on

    async def async_update(self):
        """Update the DST sensor state."""
        self._attr_is_on = self._check_dst()


class WTimeWeekdayBinarySensor(BinarySensorEntity):
    """Representation of a WTime Weekday binary sensor."""

    def __init__(self, entry_id: str):
        """Initialize the Weekday sensor."""
        self._attr_name = "WTime Is Weekday"
        self._attr_unique_id = f"{entry_id}_weekday"
        self._attr_is_on = self._check_weekday()

    def _check_weekday(self) -> bool:
        """Check if today is a weekday (Mon–Fri)."""
        try:
            now = _now_local()
            is_weekday = now.weekday() < 5  # Monday (0) .. Friday (4)
            _LOGGER.debug("Current local time: %s, Is weekday: %s", now, is_weekday)
            return is_weekday
        except Exception as err:
            _LOGGER.error("Error checking weekday status: %s", err)
            return False

    @property
    def is_on(self) -> bool:
        """Return True if today is a weekday."""
        return self._attr_is_on

    async def async_update(self):
        """Update the Weekday sensor state."""
        self._attr_is_on = self._check_weekday()


class WTimeWeekendBinarySensor(BinarySensorEntity):
    """Representation of a WTime Weekend binary sensor."""

    def __init__(self, entry_id: str):
        """Initialize the Weekend sensor."""
        self._attr_name = "WTime is Weekend"
        self._attr_unique_id = f"{entry_id}_weekend"
        self._attr_is_on = self._check_weekend()

    def _check_weekend(self) -> bool:
        """Check if today is a weekend (Sat–Sun)."""
        try:
            now = _now_local()
            is_weekend = now.weekday() >= 5  # Saturday (5), Sunday (6)
            _LOGGER.debug("Current local time: %s, Is weekend: %s", now, is_weekend)
            return is_weekend
        except Exception as err:
            _LOGGER.error("Error checking weekend status: %s", err)
            return False

    @property
    def is_on(self) -> bool:
        """Return True if today is a weekend."""
        return self._attr_is_on

    async def async_update(self):
        """Update the Weekend sensor state."""
        self._attr_is_on = self._check_weekend()


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
