from datetime import datetime
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

DOMAIN = "wtime"

SENSORS = {
    "wtime_date": {"format": "%B %d, %Y", "icon": "mdi:calendar"},
    "wtime_date_numbers": {"format": "%x", "icon": "mdi:numeric"},
    "wtime_time": {"format": "%-I:%M %p", "icon": "mdi:clock"},
    "wtime_date_time": {"format": "%B %d, %Y - %-I:%M %p", "icon": "mdi:calendar-clock"},
    "wtime_week_day_long": {"format": "%A", "icon": "mdi:calendar-today"},
    "wtime_week_day_short": {"format": "%a", "icon": "mdi:calendar-today"},
    "wtime_current_month": {"format": "%B", "icon": "mdi:calendar-month"},
    "wtime_current_season": {"format": None, "icon": "mdi:weather-partly-cloudy"},
    "wtime_jewish_week_date": {"format": None, "icon": "mdi:star-david"},
    "wtime_jewish_week_date_full": {"format": None, "icon": "mdi:star-david"},
    "wtime_timer": {"format": None, "icon": "mdi:timer-sand"}  # Added the timer sensor
}

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up Wtime sensors."""
    async_add_entities(
        WtimeSensor(name, data, entry.entry_id) for name, data in SENSORS.items()
    )


class WTimeSensor(SensorEntity):
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
        jewish_weekdays = ["א", "ב", "ג", "ד", "ה", "ו", "שבת"]
        jewish_weekdays_full = [
            "זונטאג",
            "מאנטאג",
            "דינסטאג",
            "מיטוואך",
            "דאנערשטיג",
            "פרייטאג",
            "שבת קודש",
        ]
        months = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December",
        ]
        seasons = ["Winter", "Spring", "Summer", "Fall"]
        weekdays_short = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        weekdays_long = [
            "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday",
        ]

        now = datetime.now()
        month = now.month
        weekday = (now.weekday() + 1) % 7  # Adjust for Sunday as the start of the week.

        # Determine the current season based on the month
        if month in [12, 1, 2]:
            season = "Winter"
        elif month in [3, 4, 5]:
            season = "Spring"
        elif month in [6, 7, 8]:
            season = "Summer"
        else:
            season = "Fall"

        if self._attr_name == "Wtime Jewish Week Date":
            return jewish_weekdays[weekday]
        elif self._attr_name == "Wtime Jewish Week Date Full":
            return jewish_weekdays_full[weekday]
        elif self._attr_name == "Wtime Week Day Long":
            return weekdays_long[weekday]
        elif self._attr_name == "Wtime Week Day Short":
            return weekdays_short[weekday]
        elif self._attr_name == "Wtime Current Month":
            return months[month - 1]
        elif self._attr_name == "Wtime Current Season":
            return season
        elif self._attr_name == "Wtime Timer":
            return self._state  # Return the timer value as needed
        return now.strftime(self._format)

    async def async_update(self):
        """Update the sensor state."""
        if self._attr_name == "Wtime Timer":
            self._state = datetime.now().strftime("%H:%M:%S")  # Example of updating time for the timer sensor
