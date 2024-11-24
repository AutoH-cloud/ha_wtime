from datetime import datetime
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

DOMAIN = "wtime"

SENSORS = {
    "wtime_date": {"format": "%B %d, %Y", "icon": "mdi:calendar"},
    "wtimw_date_numbers": {"format": "%x", "icon": "mdi:numeric"},
    "wtime_time": {"format": "%-I:%M %p", "icon": "mdi:clock"},
    "wtime_week_day": {"format": "%A", "icon": "mdi:calendar-today"},
    "wtime_week_day_short": {"format": "%a", "icon": "mdi:calendar-today"},
    "wtime_jewish_week_date_short": {"format": None, "icon": "mdi:star-david"},
    "wtime_jewish_week_date": {"format": None, "icon": "mdi:star-david"},
    "wtime_current_month": {"format": "%B", "icon": "mdi:calendar-month"},
    "wtime_current_season": {"format": None, "icon": "mdi:weather-partly-cloudy"},
}

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up Wtime sensors."""
    async_add_entities(
        WtimeSensor(name, data, entry.entry_id) for name, data in SENSORS.items()
    )

class WtimeSensor(SensorEntity):
    """Representation of a Wtime sensor."""

    def __init__(self, name, data, entry_id):
        self._attr_name = name.replace("_", " ").title()
        self._attr_unique_id = f"{entry_id}_{name}"
        self._format = data["format"]
        self._attr_icon = data["icon"]
        self._state = None
        self._options = self._get_options()

    @property
    def native_value(self):
        """Return the state of the sensor."""
        now = datetime.now()

        if self._attr_name in ["WTime Jewish Week Date Short", "WTime Jewish Week Date"]:
            weekday = (now.weekday() + 1) % 7  # Shift to align with Jewish weekdays
            return self._options[weekday]
        elif self._attr_name == "WTime Week Day":
            return self._options[now.weekday()]
        elif self._attr_name == "WTime Week Day Short":
            return self._options[now.weekday()]
        elif self._attr_name == "WTime Current Month":
            return self._options[now.month - 1]
        elif self._attr_name == "WTime Current Season":
            month = now.month
            if month in [12, 1, 2]:
                return "Winter"
            elif month in [3, 4, 5]:
                return "Spring"
            elif month in [6, 7, 8]:
                return "Summer"
            else:
                return "Fall"
        else:
            return now.strftime(self._format)

    @property
    def options(self):
        """Return predefined options for dropdown menus."""
        return self._options

    def _get_options(self):
        """Return predefined options for dropdown menus."""
        wtime_jewish_weekdays = ["זונטאג", "מאנטאג", "דינסטאג", "מיטוואך", "דאנערשטיג", "פרייטאג", "שבת"]
        wtime_jewish_weekdays_short = ["א", "ב", "ג", "ד", "ה", "ו", "שבת"]
        wtime_months = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December",
        ]
        wtime_seasons = ["Winter", "Spring", "Summer", "Fall"]
        wtime_weekdays_short = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        wtime_weekdays = [
            "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday",
        ]

        if self._attr_name == "WTime Jewish Week Date":
            return wtime_jewish_weekdays_short
        elif self._attr_name == "WTime Jewish Week Date":
            return wtime_jewish_weekdays
        elif self._attr_name == "WTimeWeek Day":
            return wtime_weekdays
        elif self._attr_name == "WTime Week Day Short":
            return wtime_weekdays_short
        elif self._attr_name == "Wtime Current Month":
            return wtime_months
        elif self._attr_name == "WTime Current Season":
            return seasons
        return []

    async def async_update(self):
        """Update the sensor state."""
        self._state = self.native_value
