from datetime import datetime
from homeassistant.components.sensor import SensorEntity
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
    "dst_status": {"format": None, "icon": "mdi:clock-alert"},
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
        elif self._attr_name == "Dst Status":
            # Return textual representation for DST
            return "After DST" if datetime.now().timetuple().tm_isdst == 1 else "Before DST"
        else:
            return datetime.now().strftime(self._format)

    @property
    def extra_state_attributes(self):
        """Return additional attributes for the entity."""
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
        elif self._attr_name == "Dst Status":
            return {"options": ["Before DST", "After DST"]}
        return None

    @property
    def device_class(self):
        """Define the device class for dropdown compatibility."""
        if self._attr_name in ["Jewish Week Date", "Jewish Week Date Full", "Dst Status"]:
            return "enum"
        return None

    @property
    def options(self):
        """Define dropdown options for the sensor."""
        if self._attr_name == "Jewish Week Date":
            return ["א", "ב", "ג", "ד", "ה", "ו", "שבת"]
        elif self._attr_name == "Jewish Week Date Full":
            return [
                "זונטאג",
                "מאנטאג",
                "דינסטאג",
                "מיטוואך",
                "דאנערשטיג",
                "פרייטאג",
                "שבת קודש",
            ]
        elif self._attr_name == "Dst Status":
            return ["Before DST", "After DST"]
        return None

    async def async_update(self):
        """Update the sensor state."""
        self._state = self.native_value
