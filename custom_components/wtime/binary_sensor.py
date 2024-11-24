from datetime import datetime
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory

DOMAIN = "WTime"

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up WTime binary sensors."""
    async_add_entities([WTimeDSTBinarySensor(entry.entry_id)])

class WTimeDSTBinarySensor(BinarySensorEntity):
    """Representation of a DST sensor."""

    def __init__(self, entry_id):
        self._attr_name = "DST Status"
        self._attr_unique_id = f"{entry_id}_dst_status"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._state = None

    @property
    def is_on(self):
        """Return true if the DST status is on."""
        now = datetime.now()
        self._state = now.dst() is not None
        return self._state

    async def async_update(self):
        """Update the binary sensor state."""
        pass
