from datetime import datetime
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.update_coordinator import CoordinatorEntity

DOMAIN = "wtime"

SENSORS = {
    "date": {"format": "%B %d, %Y", "icon": "mdi:calendar"},
    "date_numbers": {"format": "%x", "icon": "mdi:numeric"},
    "time": {"format": "%-I:%M %p", "icon": "mdi:clock"},
    "date_time": {"format": "%B %d, %Y - %-I:%M %p", "icon": "mdi:calendar-clock"},
    "week_day_long": {"format": "%A", "icon": "mdi:calendar-today"},
    "week_day_short": {"format": "%a", "icon": "mdi:calendar-today"},
    "week_and_date": {"format": "%a, %B %d, %Y", "icon": "mdi:calendar-range"},
    "jewish_calendar_week_date": {"format": None, "icon": "mdi:star-david"},
    "jewish_calendar_week_date_full": {"format": None, "icon": "mdi:star-david"},
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
        if self._attr_name == "Jewish Calendar Week Date":
            return ["א", "'ב", "'ג", "'ד", "'ה", "'ו", "שבת'"][
                datetime.now().weekday()
            ]
        elif self._attr_name == "Jewish Calendar Week Date Full":
            return [
                "זונטאג",
                "מאנטאג",
                "דינסטאג",
                "מיטוואך",
                "דאנערשטיג",
                "פרייטאג",
                "שבת קודש",
            ][datetime.now().weekday()]
        else:
            return datetime.now().strftime(self._format)

    async def async_update(self):
        """Update the sensor state."""
        self._state = self.native_value
