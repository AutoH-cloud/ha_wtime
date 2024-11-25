from datetime import datetime
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

DOMAIN = "wtime"

SENSORS = {
    "wtime_date": {"format": "%B %d, %Y", "icon": "mdi:calendar"},
    "wtime_date_numbers": {"format": "%x", "icon": "mdi:numeric"},
    "wtime_time": {"format": "%-I:%M %p", "icon": "mdi:clock"},
    "wtime_week_day": {"format": "%A", "icon": "mdi:calendar-today"},
    "wtime_week_day_short": {"format": "%a", "icon": "mdi:calendar-today"},
    "wtime_current_month": {"format": "%B", "icon": "mdi:calendar-month"},
    "wtime_current_season": {"format": None, "icon": "mdi:weather-partly-cloudy"},
}

SEASON_OPTIONS = ["Winter", "Spring", "Summer", "Fall"]
MONTH_OPTIONS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up WTime sensors and selects."""
    sensors = [
        WtimeSensor(name, data, entry.entry_id) for name, data in SENSORS.items()
    ]
    selects = [
        WtimeSelect("Wtime Current Month", MONTH_OPTIONS, entry.entry_id),
        WtimeSelect("Wtime Current Season", SEASON_OPTIONS, entry.entry_id),
    ]
    async_add_entities(sensors + selects, update_before_add=True)


class WtimeSensor(SensorEntity):
    """Representation of a WTime sensor."""

    def __init__(self, name, data, entry_id):
        self._attr_name = name.replace("_", " ").title()
        self._attr_unique_id = f"{entry_id}_{name}"
        self._format = data["format"]
        self._attr_icon = data["icon"]

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

        if self._attr_name == "Wtime Week Day":
            return now.strftime("%A")
        elif self._attr_name == "Wtime Week Day Short":
            return now.strftime("%a")
        elif self._attr_name == "Wtime Current Month":
            return now.strftime("%B")
        elif self._attr_name == "Wtime Current Season":
            return season
        else:
            return now.strftime(self._format)

    @property
    def extra_state_attributes(self):
        """Provide extra attributes."""
        if self._attr_name == "Wtime Current Month":
            return {"options": MONTH_OPTIONS}
        elif self._attr_name == "Wtime Current Season":
            return {"options": SEASON_OPTIONS}
        return None

    async def async_update(self):
        """Update the sensor state."""
        self._attr_native_value = self.native_value


class WtimeSelect(SelectEntity):
    """Representation of a WTime select entity."""

    def __init__(self, name, options, entry_id):
        self._attr_name = name.replace("_", " ").title()
        self._attr_unique_id = f"{entry_id}_{name}"
        self._options = options
        self._attr_options = options
        self._attr_current_option = options[0]

    async def async_select_option(self, option: str):
        """Change the selected option."""
        if option in self._options:
            self._attr_current_option = option
            self.async_write_ha_state()
