from datetime import datetime
from homeassistant.helpers.entity import Entity

# Helper function for Jewish Weekday
def jewish_weekday():
    todayyid = ["א", "'ב", "'ג", "'ד", "'ה", "'ו", "שבת"]
    return todayyid[datetime.now().weekday()]

# Helper function for Jewish Full Weekday
def jewish_weekday_full():
    todayyid_full = ["זונטאג", "מאנטאג", "דינסטאג", "מיטוואך", "דאנערשטיג", "פרייטאג", "שבת קודש"]
    return todayyid_full[datetime.now().weekday()]

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Jewish Dates sensor."""
    async_add_entities([JewishWeekdaySensor(), JewishWeekdayFullSensor()])


class JewishWeekdaySensor(Entity):
    """Sensor for Jewish weekday name."""

    def __init__(self):
        self._state = None
        self._name = "Jewish Weekday"

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return jewish_weekday()


class JewishWeekdayFullSensor(Entity):
    """Sensor for Jewish full weekday name."""

    def __init__(self):
        self._state = None
        self._name = "Jewish Full Weekday"

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return jewish_weekday_full()

