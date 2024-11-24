from datetime import datetime
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.binary_sensor import BinarySensorEntity
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
    "jewish_week_date": {"format": None, "icon": "mdi:star-david"},
    "jewish_week_date_full": {"format": None, "icon": "mdi:star-david"},
}

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up Wtime sensors and binary sensors."""
    # Add regular sensors
    async_add_entities(
        WtimeSensor(name, data, entry.entry_id) for name, data in SENSORS.items()
    )

    # Add DST binary sensor
    async_add_entities([DSTBinarySensor(entry.entry_id)])


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

        weekday = (datetime.now().weekday() + 1) % 7

        if self._attr_name == "Jewish Week Date":
            return jewish_weekdays[weekday]
        elif self._attr_name == "Jewish Week Date Full":
            return jewish_weekdays_full[weekday]
        else:
            return datetime.now().strftime(self._format)

    @property
    def extra_state_attributes(self):
        """Return additional attributes for dropdown support."""
        if self._attr_name == "Jewish Week Date":
            return {"options": ["א", "ב", "ג", "ד", "ה", "ו", "שבת"]}
        elif self._attr_name == "Jewish Week Date Full":
            return {
                "options": [
                    "זונטאג",
                    "מאנטאג",
                    "דינסטאג",
                    "מיטוואך",
                    "דאנערשטיג",
                    "פרייטאג",
                    "שבת קודש",
                ]
            }
        return None

    async def async_update(self):
        """Update the sensor state."""
        self._state = self.native_value


class DSTBinarySensor(BinarySensorEntity):
    """Representation of a binary sensor for DST status."""

    def __init__(self, entry_id):
        self._attr_name = "DST Status"
        self._attr_unique_id = f"{entry_id}_dst_status"
        self._attr_icon = "mdi:clock-alert"
        self._state = None

    @property
    def is_on(self):
        """Return True if DST is active, False otherwise."""
        return datetime.now().timetuple().tm_isdst == 1

    @property
    def extra_state_attributes(self):
        """Return additional attributes for the DST sensor."""
        return {
            "description": "Indicates whether the system is currently in Daylight Savings Time.",
            "active": "DST is currently active." if self.is_on else "DST is not active.",
        }

    async def async_update(self):
        """Update the binary sensor state."""
        self._state = self.is_on
