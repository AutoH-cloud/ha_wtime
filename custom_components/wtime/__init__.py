"""Initialize the wtime integration."""
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up WTime integration from a config entry."""
    _LOGGER.info("Setting up WTime integration")
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload WTime integration."""
    _LOGGER.info("Unloading WTime integration")
    if DOMAIN in hass.data:
        hass.data.pop(DOMAIN)
    return True
