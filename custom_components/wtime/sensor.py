from datetime import datetime
from homeassistant.helpers.entity import Entity

SEASONS = {
    1: "Winter",
    2: "Winter",
    3: "Spring",
    4: "Spring",
    5: "Spring",
    6: "Summer",
    7: "Summer",
    8: "Summer",
    9: "Fall",
    10: "Fall",
    11: "Fall",
    12: "Winter",
}

def get_current_season():
    month = datetime.now().month
    return SEASONS[month]


class WTimeSensor(Entity):
    def __init__(self, name, format_str, icon):
        self._name = name
        self._format = format_str
        self._icon = icon
        self._state = None
        self._attributes = {}

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def icon(self):
        return self._icon

    @property
    def extra_state_attributes(self):
        return self._attributes

    def update(self):
        now = datetime.now()
        if self._name == "WTime Current Season":
            self._state = get_current_season()
            self._attributes = {
                "Winter": "December, January, February",
                "Spring": "March, April, May",
                "Summer": "June, July, August",
                "Fall": "September, October, November",
            }
        elif self._format:
            self._state = now.strftime(self._format)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    sensors = [
        WTimeSensor("WTime Date", "%B %d, %Y", "mdi:calendar"),
        WTimeSensor("WTime Date Numbers", "%x", "mdi:numeric"),
        WTimeSensor("WTime Week Day", "%A", "mdi:calendar-today"),
        WTimeSensor("WTime Week Day Short", "%a", "mdi:calendar-today"),
        WTimeSensor("WTime Current Month", "%B", "mdi:calendar-month"),
        WTimeSensor("WTime Current Season", None, "mdi:weather-partly-cloudy"),
    ]
    async_add_entities(sensors, update_before_add=True)
