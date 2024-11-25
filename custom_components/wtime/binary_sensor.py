from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from datetime import datetime
import pytz
import logging

_LOGGER = logging.getLogger(__name__)

DOMAIN = "wtime"

class WTimeDSTBinarySensor(BinarySensorEntity):
    """Representation of a WTime DST binary sensor."""

    def __init__(self, entry_id: str, timezone: str):
        """Initialize the DST sensor."""
        self._attr_name = "WTime DST Status"
        self._attr_unique_id = f"{entry_id}_dst_active"
        self._timezone = pytz.timezone(timezone)  # Use Home Assistant's timezone
        self._attr_is_on = self._check_dst()

    def _check_dst(self) -> bool:
        """Check if Daylight Saving Time (DST) is active."""
        try:
            now = datetime.now(self._timezone)
            dst_offset = now.dst()  # Get DST offset
            _LOGGER.debug(f"Current time: {now}, DST offset: {dst_offset}")
            return dst_offset is not None and dst_offset != timedelta(0)  # DST active if offset is non-zero
        except Exception as e:
            _LOGGER.error(f"Error checking DST status: {e}")
            return False

    @property
    def is_on(self) -> bool:
        """Return True if DST is active."""
        return self._attr_is_on

    async def async_update(self):
        """Update the DST sensor state."""
        self._attr_is_on = self._check_dst()


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up the WTime DST binary sensor."""
    # Retrieve timezone from Home Assistant configuration
    timezone = hass.config.time_zone or "UTC"
    _LOGGER.debug(f"Setting up WTimeDSTBinarySensor with timezone: {timezone}")
    async_add_entities([WTimeDSTBinarySensor(entry.entry_id, timezone)])
