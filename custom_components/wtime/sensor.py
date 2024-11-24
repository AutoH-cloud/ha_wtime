from datetime import datetime
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

DOMAIN = "wtime"

SENSORS = {
    "current_month": {"icon": "mdi:calendar-month"},
    "current_season": {"icon": "mdi:weather-partly-cloudy"},
    "week_day_long": {"icon": "mdi:calendar-today"},
    "week_day_short": {"icon": "mdi:calendar-today"},
    "jewish_week_date": {"icon": "mdi:star-david"},
    "jewish_week_date_full": {"icon": "mdi:star-david"},
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
        self._attr_icon = data["icon"]
        self._state = None
        self._options = self._get_options()

    @property
    def native_value(self):
        """Return the current state of the sensor."""
        now = datetime.now()

        if self._attr_name == "Current Month":
            return self._options[now.month - 1]  # Month index starts at 1
        elif self._attr_name == "Current Season":
            month = now.month
            if month in [12, 1, 2]:
                return "Winter"
            elif month in [3, 4, 5]:
                return "Spring"
            elif month in [6, 7, 8]:
                return "Summer"
            else:
                return "Fall"
        elif self._attr_name == "Week Day Long":
            return self._options[now.weekday()]  # Monday is 0
        elif self._attr_name == "Week Day Short":
            return self._options[now.weekday()]
        elif self._attr_name == "Jewish Week Date":
            weekday = (now.weekday() + 1) % 7  # Shift weekday for Jewish format
            return self._options[weekday]
        elif self._attr_name == "Jewish Week Date Full":
            weekday = (now.weekday() + 1) % 7
            return self._options[weekday]
        return None

    @property
    def extra_state_attributes(self):
        """Provide dropdown options as additional attributes."""
        if self._options:
            return {"options": self._options}
        return None

    def _get_options(self):
        """Return predefined options for dropdown menus."""
        jewish_weekdays = ["זונטאג", "מאנטאג", "דינסטאג", "מיטוואך", "דאנערשטיג", "פרייטאג", "שבת"]
        jewish_weekdays_short = ["א", "ב", "ג", "ד", "ה", "ו", "שבת"]
        months = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December",
        ]
        seasons = ["Winter", "Spring", "Summer", "Fall"]
        weekdays_short = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        weekdays_long = [
            "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday",
        ]

        if self._attr_name == "Jewish Week Date":
            return jewish_weekdays_short
        elif self._attr_name == "Jewish Week Date Full":
            return jewish_weekdays
        elif self._attr_name == "Current Month":
            return months
        elif self._attr_name == "Current Season":
            return seasons
        elif self._attr_name == "Week Day Long":
            return weekdays_long
        elif self._attr_name == "Week Day Short":
            return weekdays_short
        return []

    async def async_update(self):
        """Update the sensor state."""
        self._state = self.native_value
