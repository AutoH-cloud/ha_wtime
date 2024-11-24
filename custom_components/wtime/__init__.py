"""WTime integration for Home Assistant."""

from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

DOMAIN = "wtime"

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the WTime component."""
    hass.data[DOMAIN] = {}
    return True

async def async_setup_entry(hass: HomeAssistant, entry) -> bool:
    """Set up WTime from a config entry."""
    return True

async def async_unload_entry(hass: HomeAssistant, entry) -> bool:
    """Unload a WTime config entry."""
    return True

