from homeassistant.helpers.entity import Entity
from datetime import datetime

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the DST sensor."""
    async_add_entities([DSTSensor()])


class DSTSensor(Entity):
    """Sensor to check if DST is active."""

    def __init__(self):
        self._state = None
        self._name = "DST Status"

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return "After DST" if datetime.now().timetuple().tm_isdst == 1 else "Before DST"

