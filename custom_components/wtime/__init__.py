"""Initialize the wdate integration."""
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the wdate integration."""
    # Perform any necessary initialization here
    _LOGGER.info("Setting up the wdate integration")
    return True
