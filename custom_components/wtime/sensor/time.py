from datetime import datetime
from homeassistant.helpers.entity import Entity

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Time sensor."""
    async_add_entities([TimeSensor()])


class TimeSensor(Entity):
    """Sensor to display the current time."""

    def __init__(self):
        self._state = None
        self._name = "Time"

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return datetime.now().strftime('%I:%M %p')  # Current time in 12-hour format

