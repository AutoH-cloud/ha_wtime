# custom_components/WTime/binary_sensor.py
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from datetime import datetime
from .const import DOMAIN

class WTimeDSTBinarySensor(BinarySensorEntity):
    """Representation of a WTime DST binary sensor."""

    def __init__(self, entry_id: str):
        self._attr_name = "DST Active"
        self._attr_unique_id = f"{entry_id}_dst_active"
        self._attr_is_on = self._check_dst()

    def _check_dst(self) -> bool:
        """Check if Daylight Saving Time is active."""
        now = datetime.now()
        return now.dst() != timedelta(0)  # If the DST offset is non-zero, DST is active

    @property
    def is_on(self) -> bool:
        """Return true if DST is currently active."""
        return self._attr_is_on

    async def async_update(self):
        """Update the state of the DST binary sensor."""
        self._attr_is_on = self._check_dst()
        self.async_schedule_update_ha_state()

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up the DST binary sensor for WTime."""
    binary_sensor = WTimeDSTBinarySensor(entry_id=entry.entry_id)
    async_add_entities([binary_sensor])
