from datetime import datetime
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

DOMAIN = "wtime"

# Define possible states
MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

SEASONS = ["Winter", "Spring", "Summer", "Fall"]

WEEKDAYS = [
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
]

SENSORS = {
    "wtime_date": {"format": "%B %d, %Y", "icon": "mdi:calendar"},
    "wtime_date_short": {"format": "%x", "icon": "mdi:numeric"},
    "wtime_clock": {"format": "%-I:%M %p", "icon": "mdi:clock"},
    "wtime_weekday": {"format": "%A", "icon": "mdi:calendar-today", "possible_states": WEEKDAYS},
    "wtime_weekday_short": {"format": "%a", "icon": "mdi:calendar-today"},
    "wtime_current_month": {"format": "%B", "icon": "mdi:calendar-month", "possible_states": MONTHS},
    "wtime_current_season": {"format": None, "icon": "mdi:weather-partly-cloudy", "possible_states": SEASONS},
}

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up WTime sensors."""
    async_add_entities(
        WtimeSensor(name, data, entry.entry_id) for name, data in SENSORS.items()
    )

class WtimeSensor(SensorEntity):
    """Representation of a WTime sensor."""

    def __init__(self, name, data, entry_id):
        self._attr_name = name.replace("_", " ").title()
        self._attr_unique_id = f"{entry_id}_{name}"
        self._format = data["format"]
        self._attr_icon = data["icon"]
        self._possible_states = data.get("possible_states", None)

    @property
    def native_value(self):
        """Return the state of the sensor."""
        now = datetime.now()
        month = now.month

        # Determine the current season based on the month
        if month in [12, 1, 2]:
            season = "Winter"
        elif month in [3, 4, 5]:
            season = "Spring"
        elif month in [6, 7, 8]:
            season = "Summer"
        else:
            season = "Fall"

        if self._attr_name == "Wtime Weekday":
            return now.strftime("%A")
        elif self._attr_name == "Wtime Weekday Short":
            return now.strftime("%a")
        elif self._attr_name == "Wtime Current Month":
            return now.strftime("%B")
        elif self._attr_name == "Wtime Current Season":
            return season
        else:
            return now.strftime(self._format)

    @property
    def extra_state_attributes(self):
        """Add possible states as attributes."""
        attributes = {}
        if self._possible_states:
            attributes["possible_states"] = self._possible_states
        return attributes

    async def async_update(self):
        """Update the sensor state."""
        self._attr_native_value = self.native_value
