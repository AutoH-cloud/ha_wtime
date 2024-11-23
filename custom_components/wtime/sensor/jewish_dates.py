from datetime import datetime
from homeassistant.components.sensor import SensorEntity


def jewish_weekday():
    """Get the Jewish weekday (short form)."""
    todayyid = ["א", "ב", "ג", "ד", "ה", "ו", "שבת"]
    return todayyid[datetime.now().weekday()]


def jewish_weekday_full():
    """Get the Jewish weekday (full form)."""
    todayyid_full = [
        "זונטאג",
        "מאנטאג",
        "דינסטאג",
        "מיטוואך",
        "דאנערשטיג",
        "פרייטאג",
        "שבת קודש",
    ]
    return todayyid_full[datetime.now().weekday()]


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Jewish Dates sensors."""
    async_add_entities([JewishWeekdaySensor(), JewishWeekdayFullSensor()])


class JewishWeekdaySensor(SensorEntity):
    """Sensor to display the Jewish weekday (short form)."""

    def __init__(self):
        """Initialize the sensor."""
        self._attr_name = "Jewish Weekday"

    @property
    def native_value(self):
        """Return the current Jewish weekday (short)."""
        return jewish_weekday()


class JewishWeekdayFullSensor(SensorEntity):
    """Sensor to display the Jewish weekday (full form)."""

    def __init__(self):
        """Initialize the sensor."""
        self._attr_name = "Jewish Full Weekday"

    @property
    def native_value(self):
        """Return the current Jewish weekday (full)."""
        return jewish_weekday_full()
