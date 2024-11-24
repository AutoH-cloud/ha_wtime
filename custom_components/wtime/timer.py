from datetime import timedelta
import logging

from homeassistant.components.timer import TimerEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, State
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.event import async_call_later

_LOGGER = logging.getLogger(__name__)

DOMAIN = "WTime"

# Define the number of timers
MAX_TIMERS = 10

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up WTime timers."""
    timers = []
    for i in range(MAX_TIMERS):
        timers.append(WTimeTimer(entry.entry_id, i))

    async_add_entities(timers)


class WTimeTimer(TimerEntity):
    """Representation of a WTime Timer."""

    def __init__(self, entry_id, timer_id):
        self._entry_id = entry_id
        self._timer_id = timer_id
        self._name = f"WTime Timer {self._timer_id + 1}"
        self._state = "idle"
        self._duration = timedelta(minutes=1)  # Default to 1 minute
        self._time_left = self._duration.total_seconds()

    @property
    def name(self):
        """Return the name of the timer."""
        return self._name

    @property
    def state(self):
        """Return the state of the timer."""
        return self._state

    @property
    def icon(self):
        """Return the icon of the timer."""
        if self._state == "idle":
            return "mdi:timer-off"
        elif self._state == "active":
            return "mdi:timer"
        else:
            return "mdi:timer-sand"

    @property
    def extra_state_attributes(self):
        """Return additional attributes for the timer."""
        return {
            "duration": self._duration,
            "time_left": self._time_left,
        }

    async def async_set_timer(self, duration_minutes, name=None):
        """Set the timer duration and name."""
        self._duration = timedelta(minutes=duration_minutes)
        self._time_left = self._duration.total_seconds()
        if name:
            self._name = name

        self._state = "active"
        _LOGGER.info(f"Timer {self._name} set for {self._duration}")
        self.async_schedule_update_ha_state()

        await self._start_timer()

    async def _start_timer(self):
        """Start the timer countdown."""
        async def on_timer_finish(_):
            """Callback when timer finishes."""
            self._state = "idle"
            self._time_left = 0
            self.async_schedule_update_ha_state()

            # Trigger automation or event on timer finish
            await self._on_timer_done()

        # Schedule the timer to finish after the set duration
        async_call_later(self.hass, self._duration.total_seconds(), on_timer_finish)

    async def _on_timer_done(self):
        """Run automation or trigger an event after the timer finishes."""
        _LOGGER.info(f"Timer {self._name} has finished!")
        # Here you can call an automation, event, or any action you want to trigger.
        # For now, let's just log the completion.
        self.hass.bus.async_fire(f"{DOMAIN}_timer_done", {"timer_name": self._name})

    async def async_reset(self):
        """Reset the timer."""
        self._state = "idle"
        self._time_left = self._duration.total_seconds()
        self.async_schedule_update_ha_state()
        _LOGGER.info(f"Timer {self._name} reset.")

    async def async_start(self):
        """Start the timer."""
        if self._state == "idle":
            await self.async_set_timer(self._duration.total_seconds() / 60)
        else:
            _LOGGER.warning(f"Timer {self._name} is already running.")
