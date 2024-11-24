# custom_components/WTime/__init__.py
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the WTime component."""
    _LOGGER.debug("Setting up WTime integration")
    return True
