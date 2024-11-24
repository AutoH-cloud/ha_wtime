from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from datetime import datetime, timedelta
import pytz
import logging

_LOGGER = logging.getLogger(__name__)

DOMAIN = "wtime"

class WTimeDSTBinarySensor(BinarySensorEntity):
    """Representation of a WTime DST binary sensor."""

    def __init__(self, entry_id: str, timezone: str):
        """Initialize the DST sensor."""
        self._attr_name = "DST Status"
        self._attr_unique_id = f"{entry_id}_dst_active"
        self._timezone = pytz.timezone(timezone)  # Use the passed timezone
        self._attr_is_on = self._check_dst()

    def _check_dst(self) -> bool:
        """Check if Daylight Saving Time (DST) is active."""
        try:
            now = datetime.now(self._timezone)
            dst_active = now.dst() != timedelta(0)  # DST is active if offset is non-zero
            _LOGGER.debug(f"DST status checked: {dst_active}")
            return dst_active
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
    # Replace with the timezone you want to use
    timezone = "America/New_York"
    _LOGGER.debug(f"Setting up WTimeDSTBinarySensor with timezone: {timezone}")
    async_add_entities([WTimeDSTBinarySensor(entry.entry_id, timezone)])
