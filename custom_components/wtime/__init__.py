from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from .sensor import async_setup_entry as setup_sensors  # Import the async_setup_entry from the sensor module

_LOGGER = logging.getLogger(__name__)

DOMAIN = "wtime"

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the WTime integration."""
    _LOGGER.debug("Setting up Wtime integration")
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up WTime from a config entry."""
    _LOGGER.debug("Setting up Wtime entry")
    # Ensure you pass async_add_entities to the sensor setup
    await setup_sensors(hass, entry, hass.helpers.entity_platform.async_add_entities)
    return True
