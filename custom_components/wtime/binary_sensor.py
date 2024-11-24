from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from datetime import datetime, timedelta
from .const import DOMAIN

class WTimeDSTBinarySensor(BinarySensorEntity):
    """Representation of a WTime DST binary sensor."""

    def __init__(self, entry_id: str):
        self._attr_name = "DST Status"
        self._attr_unique_id = f"{entry_id}_dst_active"
        self._attr_is_on = self._check_dst()

    def _check_dst(self) -> bool:
        now = datetime.now()
        return now.dst() != timedelta(0)  # DST is active if offset is non-zero

    @property
    def is_on(self) -> bool:
        return self._attr_is_on

    async def async_update(self):
        self._attr_is_on = self._check_dst()

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    async_add_entities([WTimeDSTBinarySensor(entry.entry_id)])
