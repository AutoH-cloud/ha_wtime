import logging
from datetime import datetime, timedelta
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.util.dt import get_astral_event_date
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up WTime sensors."""
    async_add_entities([WTimeAstronomicalSensor(entry.entry_id)])

class WTimeAstronomicalSensor(SensorEntity):
    """Representation of an astronomical time sensor."""

    def __init__(self, entry_id):
        self._attr_name = "Next Astronomical Event"
        self._attr_unique_id = f"{entry_id}_astronomical_event"
        self._state = None
        self._next_event = None

    @property
    def native_value(self):
        """Return the next astronomical event."""
        return self._state

    async def async_update(self):
        """Update the sensor to show the next astronomical event."""
        now = datetime.now()
        events = ["sunrise", "sunset", "dawn", "dusk"]
        next_events = {
            event: get_astral_event_date(self.hass, event, now) for event in events
        }
        self._next_event = min(next_events, key=lambda k: next_events[k])
        self._state = f"{self._next_event.capitalize()} at {next_events[self._next_event].time()}"
