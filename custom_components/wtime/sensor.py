from datetime import datetime, timedelta
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, CoordinatorEntity
import logging

_LOGGER = logging.getLogger(__name__)

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
    "wtime_date": {"format": "%B %d, %Y", "icon": "mdi:calendar", "possible_states": None},
    "wtime_date_short": {"format": "%x", "icon": "mdi:numeric", "possible_states": None},
    "wtime_12hr_clock": {"format": "%-I:%M %p", "icon": "mdi:clock", "possible_states": None},
    "wtime_weekday": {"format": "%A", "icon": "mdi:calendar-today", "possible_states": WEEKDAYS, "device_class": "enum"},
    "wtime_weekday_short": {"format": "%a", "icon": "mdi:calendar-today", "possible_states": None},
    "wtime_current_month": {"format": "%B", "icon": "mdi:calendar-month", "possible_states": MONTHS, "device_class": "enum"},
    "wtime_current_season": {"format": None, "icon": "mdi:weather-partly-cloudy", "possible_states": SEASONS, "device_class": "enum"},
    "wtime_24hr_clock": {"format": "%H:%M", "icon": "mdi:clock-outline", "possible_states": None},
    "wtime_12hr_clock_with_seconds": {"format": "%-I:%M:%S %p", "icon": "mdi:clock-time-four-outline", "possible_states": None},
    "wtime_24hr_clock_with_seconds": {"format": "%H:%M:%S", "icon": "mdi:clock-digital", "possible_states": None},
}

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up WTime sensors."""

    async def async_update_data():
        """Fetch data for the sensors."""
        return datetime.now()

    # Coordinator for managing updates
    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="WTime Update Coordinator",
        update_method=async_update_data,
        update_interval=timedelta(seconds=1),  # Update every second for real-time clock
    )

    await coordinator.async_config_entry_first_refresh()

    # Add sensors
    sensors = [
        WtimeSensor(name, data, coordinator, entry.entry_id)
        for name, data in SENSORS.items()
    ]
    async_add_entities(sensors, update_before_add=True)

class WtimeSensor(CoordinatorEntity, SensorEntity):
    """Representation of a WTime sensor."""

    def __init__(self, name, data, coordinator, entry_id):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_name = name.replace("_", " ").title()
        self._attr_unique_id = f"{entry_id}_{name}"
        self._format = data["format"]
        self._attr_icon = data["icon"]
        self._possible_states = data.get("possible_states")
        self._device_class = data.get("device_class")
        self._attr_native_value = None

    @property
    def native_value(self):
        """Return the current state of the sensor."""
        now = self.coordinator.data  # Get the latest time from the coordinator
        month = now.month

        if self._attr_name == "Wtime Weekday":
            return now.strftime("%A")  # Matches WEEKDAYS
        elif self._attr_name == "Wtime Weekday Short":
            return now.strftime("%a")  # Short weekday
        elif self._attr_name == "Wtime Current Month":
            return now.strftime("%B")  # Matches MONTHS
        elif self._attr_name == "Wtime Current Season":
            if month in [12, 1, 2]:
                return "Winter"
            elif month in [3, 4, 5]:
                return "Spring"
            elif month in [6, 7, 8]:
                return "Summer"
            else:
                return "Fall"  # Matches SEASONS
        elif self._format:
            return now.strftime(self._format)
        return None

    @property
    def extra_state_attributes(self):
        """Return additional attributes."""
        return {}

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return self._attr_icon

    @property
    def device_class(self):
        """Return the device class of the sensor."""
        return self._device_class
