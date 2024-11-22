from datetime import datetime
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

DOMAIN = "wtime"

SENSORS = {
    "date": {"format": "%B %d, %Y", "icon": "mdi:calendar"},
    "date_numbers": {"format": "%x", "icon": "mdi:numeric"},
    "time": {"format": "%-I:%M %p", "icon": "mdi:clock"},
    "date_time": {"format": "%B %d, %Y - %-I:%M %p", "icon": "mdi:calendar-clock"},
    "week_day_long": {"format": "%A", "icon": "mdi:calendar-today"},
    "week_day_short": {"format": "%a", "icon": "mdi:calendar-today"},
    "week_and_date": {"format": "%a, %B %d, %Y", "icon": "mdi:calendar-range"},
    "jewish_calendar_week_date": {"format": None, "icon": "mdi:star-david"},
    "jewish_calendar_week_date_full": {"format": None, "icon": "mdi:star-david"}
}

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up Wtime sensors."""
    sensors = [WtimeSensor(name, data) for name, data in SENSORS.items()]
    async_add_entities(sensors, update_before_add=True)

class WtimeSensor(SensorEntity):
    """Representation of a Wtime sensor."""

    def __init__(self, name, data):
        self._name = name.replace("_", " ").title()
        self._format = data["format"]
        self._icon = data["icon"]
        self._state = None

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def icon(self):
        return self._icon

    async def async_update(self):
        """Update the sensor state."""
        if self._name == "Jewish Calendar Week Date":
            self._state = ["א", "'ב", "'ג", "'ד", "'ה", "'ו", "שבת'"][
                datetime.now().weekday()
            ]
        elif self._name == "Jewish Calendar Week Date Full":
            self._state = [
                "זונטאג",
                "מאנטאג",
                "דינסטאג",
                "מיטוואך",
                "דאנערשטיג",
                "פרייטאג",
                "שבת קודש",
            ][datetime.now().weekday()]
        else:
            self._state = datetime.now().strftime(self._format)
