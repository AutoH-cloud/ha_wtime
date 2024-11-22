from datetime import datetime
from homeassistant.helpers.entity import Entity
from homeassistant.const import DATE_FORMAT

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Date sensor."""
    async_add_entities([DateSensor()])


class DateSensor(Entity):
    """Sensor to display the current date in various formats."""

    def __init__(self):
        self._state = None
        self._name = "Date"

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return datetime.now().strftime('%B %d, %Y')  # Current date in full format

