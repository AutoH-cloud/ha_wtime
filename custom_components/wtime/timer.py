# custom_components/WTime/timer.py
from datetime import timedelta
from homeassistant.components.timer import TimerEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import Entity

class WTimeTimer(TimerEntity):
    """Representation of a WTime timer."""

    def __init__(self, name: str, entry_id: str, duration: int):
        self._attr_name = name
        self._attr_unique_id = f"{entry_id}_{name}"
        self._duration = duration
        self._state = "idle"
        self._time_left = duration

    @property
    def native_value(self):
        return self._time_left

    @property
    def duration(self):
        return timedelta(seconds=self._duration)

    async def async_start(self, duration=None):
        self._state = "active"
        self._time_left = self._duration
        self.async_schedule_update_ha_state()

    async def async_pause(self):
        self._state = "paused"
        self.async_schedule_update_ha_state()

    async def async_stop(self):
        self._state = "idle"
        self._time_left = self._duration
        self.async_schedule_update_ha_state()
