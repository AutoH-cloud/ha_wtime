"""WTime integration for Home Assistant."""

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import ConfigType

DOMAIN = "wtime"

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the WTime component."""
    hass.data[DOMAIN] = {}
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up WTime from a config entry."""
    hass.config_entries.async_setup_platforms(entry, ["sensor", "binary_sensor"])
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a WTime config entry."""
    hass.config_entries.async_unload_platforms(entry, ["sensor", "binary_sensor"])
    return True
