"""The Wtime integration."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import discovery

DOMAIN = "wtime"

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the WTime integration."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up WTime from a config entry."""
    from .sensor import async_setup_entry as setup_sensors
    await setup_sensors(hass, entry, async_add_entities)
    return True
