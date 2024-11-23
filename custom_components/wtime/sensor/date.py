from datetime import datetime
from homeassistant.components.sensor import SensorEntity

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Date sensor."""
    async_add_entities([DateSensor()])


class DateSensor(SensorEntity):
    """Sensor to display the current date in various formats."""

    def __init__(self):
        """Initialize the Date sensor."""
        self._attr_name = "Date"
        self._attr_native_value = None

    @property
    def native_value(self):
        """Return the current date."""
        return datetime.now().strftime('%B %d, %Y')  # Current date in full format
