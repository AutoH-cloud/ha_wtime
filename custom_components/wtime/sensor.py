from datetime import datetime
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

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
    def __init__(self, hass, name, format_str, icon):
        self.hass = hass
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


def setup_platform(hass, config, add_entities, discovery_info=None):
    sensors = [
        WTimeSensor(hass, "WTime Date", "%B %d, %Y", "mdi:calendar"),
        WTimeSensor(hass, "WTime Date Numbers", "%x", "mdi:numeric"),
        WTimeSensor(hass, "WTime Week Day", "%A", "mdi:calendar-today"),
        WTimeSensor(hass, "WTime Week Day Short", "%a", "mdi:calendar-today"),
        WTimeSensor(hass, "WTime Current Month", "%B", "mdi:calendar-month"),
        WTimeSensor(hass, "WTime Current Season", None, "mdi:weather-partly-cloudy"),
    ]
    add_entities(sensors)
