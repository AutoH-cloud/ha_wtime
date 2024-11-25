from datetime import datetime
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import SensorDeviceClass

DOMAIN = "wtime"

SENSORS = {
    "wtime_clock": {"format": "%-I:%M %p", "icon": "mdi:clock", "device_class": SensorDeviceClass.TIME},
    "wtime_week_day": {"format": "%A", "icon": "mdi:calendar-today"},
    "wtime_week_day_short": {"format": "%a", "icon": "mdi:calendar-today"},
    "wtime_current_month": {"format": "%B", "icon": "mdi:calendar-month"},
    "wtime_current_season": {"format": None, "icon": "mdi:weather-partly-cloudy"},
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
        self._format = data.get("format")
        self._attr_icon = data.get("icon")
        self._device_class = data.get("device_class")

    @property
    def device_class(self):
        """Return the device class of the sensor."""
        return self._device_class

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
        elif self._attr_name == "Wtime Clock":
            return now.strftime(self._format)
        else:
            return now.strftime(self._format)

    @property
    def extra_state_attributes(self):
        """Provide dropdown options for certain sensors."""
        months = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        seasons = ["Winter", "Spring", "Summer", "Fall"]
        weekdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

        if self._attr_name == "Wtime Current Month":
            return {"options": months}
        elif self._attr_name == "Wtime Current Season":
            return {"options": seasons}
        elif self._attr_name in ["Wtime Week Day", "Wtime Week Day Short"]:
            return {"options": weekdays}
        return None

    async def async_update(self):
        """Update the sensor state."""
        self._attr_native_value = self.native_value
