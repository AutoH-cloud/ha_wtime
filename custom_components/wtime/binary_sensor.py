from datetime import datetime
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory

DOMAIN = "wtime"

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up Wtime binary sensors."""
    async_add_entities([DSTBinarySensor(entry.entry_id)])

class DSTBinarySensor(BinarySensorEntity):
    """Representation of the WTime DST status sensor."""

    def __init__(self, entry_id):
        self._attr_name = "WTime DST Status"
        self._attr_unique_id = f"{entry_id}_dst_status"
        self._attr_icon = "mdi:clock-alert"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._state = None

    @property
    def is_on(self):
        """Return true if DST is active."""
        # Check if DST is active (tm_isdst == 1 means DST is active)
        return datetime.now().timetuple().tm_isdst == 1

    @property
    def extra_state_attributes(self):
        """Return additional attributes."""
        return {"DST Status": "Active" if self.is_on else "Inactive"}

    async def async_update(self):
        """Update the Wtime DST sensor state."""
        # Since `is_on` is calculated dynamically based on the current time,
        # there's no need to update the state separately.
        pass
