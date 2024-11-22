from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

DOMAIN = "wtime"

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up Wtime from configuration.yaml (not used for UI)."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Wtime from a config entry."""
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload Wtime config entry."""
    await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload Wtime config entry."""
    return await hass.config_entries.async_forward_entry_unload(entry, "sensor")

