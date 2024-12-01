from datetime import datetime, timedelta
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_track_time_interval

DOMAIN = "wtime"

MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

SEASONS = ["Winter", "Spring", "Summer", "Fall"]

WEEKDAYS = [
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
]

SENSORS = {
    "wtime_date": {"format": "%B %d, %Y", "icon": "mdi:calendar", "possible_states": None},
    "wtime_date_short": {"format": "%x", "icon": "mdi:numeric", "possible_states": None},
    "wtime_weekday": {"format": "%A", "icon": "mdi:calendar-today", "possible_states": WEEKDAYS, "device_class": "enum"},
    "wtime_weekday_short": {"format": "%a", "icon": "mdi:calendar-today", "possible_states": None},
    "wtime_current_month": {"format": "%B", "icon": "mdi:calendar-month", "possible_states": MONTHS, "device_class": "enum"},
    "wtime_current_season": {"format": None, "icon": "mdi:weather-partly-cloudy", "possible_states": SEASONS, "device_class": "enum"},
    "wtime_12hr_clock": {"format": "%-I:%M %p", "icon": "mdi:clock", "possible_states": None},
    "wtime_24hr_clock": {"format": "%H:%M", "icon": "mdi:clock-outline", "possible_states": None},
    "wtime_12hr_clock_with_seconds": {"format": "%-I:%M:%S %p", "icon": "mdi:clock-time-four-outline", "possible_states": None},
    "wtime_24hr_clock_with_seconds": {"format": "%H:%M:%S", "icon": "mdi:clock-digital", "possible_states": None},
}


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up WTime sensors."""
    sensors = [WtimeSensor(name, data, entry.entry_id) for name, data in SENSORS.items()]
    async_add_entities(sensors, update_before_add=True)


class WtimeSensor(SensorEntity):
    """Representation of a WTime sensor."""

    def __init__(self, name, data, entry_id):
        """Initialize the sensor."""
        self._attr_name = name.replace("_", " ").title()
        self._attr_unique_id = f"{entry_id}_{name}"
        self._format = data["format"]
        self._attr_icon = data["icon"]
        self._possible_states = data.get("possible_states")
        self._device_class = data.get("device_class")
        self._attr_native_value = None
        self._attr_options = self._possible_states
        self._entry_id = entry_id
        self._is_real_time = name in {
            "wtime_12hr_clock",
            "wtime_24hr_clock",
            "wtime_12hr_clock_with_seconds",
            "wtime_24hr_clock_with_seconds",
        }
        self._update_interval = timedelta(seconds=1 if "seconds" in name else 60)

    async def async_added_to_hass(self):
        """Set up interval updates for real-time sensors."""
        if self._is_real_time:
            async_track_time_interval(self.hass, self._update_real_time, self._update_interval)

    async def _update_real_time(self, _):
        """Update the state of real-time sensors."""
        self._attr_native_value = self.native_value
        self.async_schedule_update_ha_state()

    @property
    def native_value(self):
        """Return the current state of the sensor."""
        now = datetime.now()
        month = now.month

        if self._attr_name == "Wtime Weekday":
            return now.strftime("%A")
        elif self._attr_name == "Wtime Weekday Short":
            return now.strftime("%a")
        elif self._attr_name == "Wtime Current Month":
            return now.strftime("%B")
        elif self._attr_name == "Wtime Current Season":
            if month in [12, 1, 2]:
                return "Winter"
            elif month in [3, 4, 5]:
                return "Spring"
            elif month in [6, 7, 8]:
                return "Summer"
            else:
                return "Fall" 
        elif self._format:
            return now.strftime(self._format)
        return None

    @property
    def extra_state_attributes(self):
        """Return additional attributes (exclude possible_states)."""
        return {}

    @property
    def options(self):
        """Expose the predefined states as options."""
        return self._attr_options

    @property
    def device_class(self):
        """Return the device class of the sensor."""
        return self._device_class
