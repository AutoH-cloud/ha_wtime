import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers import discovery

_LOGGER = logging.getLogger(__name__)

DOMAIN = "wtime"

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the WTime integration."""
    _LOGGER.debug("Setting up Wtime integration")
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up WTime from a config entry."""
    _LOGGER.debug("Setting up Wtime entry")
    from .sensor import async_setup_entry as setup_sensors
    await setup_sensors(hass, entry, async_add_entities)
    return True
