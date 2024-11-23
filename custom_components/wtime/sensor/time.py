from datetime import datetime
from homeassistant.components.sensor import SensorEntity

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Time sensor."""
    async_add_entities([TimeSensor()])


class TimeSensor(SensorEntity):
    """Sensor to display the current time."""

    def __init__(self):
        """Initialize the sensor."""
        self._attr_name = "Time"

    @property
    def native_value(self):
        """Return the current time in 12-hour format."""
        return datetime.now().strftime('%I:%M %p')
