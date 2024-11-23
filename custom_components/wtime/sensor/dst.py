from datetime import datetime
from homeassistant.components.sensor import SensorEntity

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the DST sensor."""
    async_add_entities([DSTSensor()])


class DSTSensor(SensorEntity):
    """Sensor to check if DST is active."""

    def __init__(self):
        """Initialize the DST sensor."""
        self._attr_name = "DST Status"

    @property
    def native_value(self):
        """Return the current DST status."""
        return "After DST" if datetime.now().timetuple().tm_isdst == 1 else "Before DST"
