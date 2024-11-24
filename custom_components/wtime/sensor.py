from datetime import datetime
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

DOMAIN = "wtime"

SENSORS = {
    "date": {"format": "%B %d, %Y", "icon": "mdi:calendar"},
    "date_numbers": {"format": "%x", "icon": "mdi:numeric"},
    "time": {"format": "%-I:%M %p", "icon": "mdi:clock"},
    "week_day_long": {"format": "%A", "icon": "mdi:calendar-today"},
    "week_day_short": {"format": "%a", "icon": "mdi:calendar-today"},
    "jewish_week_date": {"format": None, "icon": "mdi:star-david"},
    "jewish_week_date_full": {"format": None, "icon": "mdi:star-david"},
    "current_month": {"format": "%B", "icon": "mdi:calendar-month"},
    "current_season": {"format": None, "icon": "mdi:weather-partly-cloudy"},
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

    @property
    def native_value(self):
        """Return the state of the sensor."""
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

        now = datetime.now()
        month = now.month
        weekday = now.weekday()

        # Adjust weekday mapping (0=Sunday, 6=Saturday) for Jewish weekdays
        jewish_weekday = (weekday + 1) % 7  # Shift Python's weekday (0=Monday) to start from Sunday

        # Determine the current season based on the month
        if month in [12, 1, 2]:
            season = "Winter"
        elif month in [3, 4, 5]:
            season = "Spring"
        elif month in [6, 7, 8]:
            season = "Summer"
        else:
            season = "Fall"

        if self._attr_name == "Jewish Week Date":
            return jewish_weekdays_short[jewish_weekday]
        elif self._attr_name == "Jewish Week Date Full":
            return jewish_weekdays[jewish_weekday]
        elif self._attr_name == "Week Day Long":
            return weekdays_long[weekday]
        elif self._attr_name == "Week Day Short":
            return weekdays_short[weekday]
        elif self._attr_name == "Current Month":
            return months[month - 1]
        elif self._attr_name == "Current Season":
            return season
        else:
            return now.strftime(self._format)

    @property
    def extra_state_attributes(self):
        """Return additional attributes for dropdown support."""
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
            return {"options": jewish_weekdays_short}
        elif self._attr_name == "Jewish Week Date Full":
            return {"options": jewish_weekdays}
        elif self._attr_name == "Week Day Long":
            return {"options": weekdays_long}
        elif self._attr_name == "Week Day Short":
            return {"options": weekdays_short}
        elif self._attr_name == "Current Month":
            return {"options": months}
        elif self._attr_name == "Current Season":
            return {"options": seasons}
        return None

    async def async_update(self):
        """Update the sensor state."""
        self._state = self.native_value
