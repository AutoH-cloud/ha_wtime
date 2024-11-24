from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from datetime import datetime, timedelta
import pytz  # Ensure pytz is available
from .const import DOMAIN

class WTimeDSTBinarySensor(BinarySensorEntity):
    """Representation of a WTime DST binary sensor."""

    def __init__(self, entry_id: str, timezone: str):
        self._attr_name = "DST Status"
        self._attr_unique_id = f"{entry_id}_dst_active"
        self._timezone = pytz.timezone(timezone)  # Use Home Assistant's timezone
        self._attr_is_on = self._check_dst()

    def _check_dst(self) -> bool:
        """Check if Daylight Saving Time (DST) is active."""
        now = datetime.now(self._timezone)
        return now.dst() != timedelta(0)  # DST is active if offset is non-zero

    @property
    def is_on(self) -> bool:
        """Return True if DST is active."""
        return self._attr_is_on

    async def async_update(self):
        """Update the DST sensor state."""
        self._attr_is_on = self._check_dst()


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up the WTime DST binary sensor."""
    # Use Home Assistant's configured timezone
    timezone = hass.config.time_zone or "UTC"  # Default to UTC if not set
    async_add_entities([WTimeDSTBinarySensor(entry.entry_id, timezone)])
