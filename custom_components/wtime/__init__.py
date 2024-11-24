"""The Wtime integration."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import discovery

DOMAIN = "wtime"

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the WTime integration."""
    # This would allow the discovery process to be handled
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up WTime from a config entry."""
    # Register your sensors here or call async_setup_entry for each sensor
    from .sensor import async_setup_entry as setup_sensors
    await setup_sensors(hass, entry, async_add_entities)
    return True
