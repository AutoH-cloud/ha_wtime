from __future__ import annotations

from datetime import timedelta
import logging
from typing import Callable, Optional

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.event import async_track_time_interval

from .const import (
    DOMAIN,
    DEFAULT_NAME,
    CONF_AUTOPURGE_ENABLED,
    CONF_AUTOPURGE_ENTITY_IDS,
    CONF_AUTOPURGE_INTERVAL,
    DEFAULT_AUTOPURGE_ENTITY_IDS,
    DEFAULT_AUTOPURGE_INTERVAL,
)

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.BINARY_SENSOR]

# Keep runtime stuff per entry here
# hass.data[DOMAIN][entry_id] = {"purge_unsub": Callable|None, "update_unsub": Callable|None}
def _get_entry_bucket(hass: HomeAssistant, entry_id: str) -> dict:
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN].setdefault(entry_id, {"purge_unsub": None, "update_unsub": None})
    return hass.data[DOMAIN][entry_id]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up WTime from a config entry."""
    dev_reg = dr.async_get(hass)

    # Device (nice name + vendor)
    device = dev_reg.async_get_device(identifiers={(DOMAIN, entry.entry_id)})
    if device is None:
        device = dev_reg.async_get_or_create(
            config_entry_id=entry.entry_id,
            identifiers={(DOMAIN, entry.entry_id)},
            name=DEFAULT_NAME,
            manufacturer="AutoH Cloud",
            model="WTime Virtual",
            sw_version="1.3.0",
        )

    # Area assignment if present in data
    area_id = entry.data.get("area_id")
    if area_id and device.area_id != area_id:
        dev_reg.async_update_device(device.id, area_id=area_id)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Start/pin the auto-purger based on options
    bucket = _get_entry_bucket(hass, entry.entry_id)
    _start_or_stop_autopurger(hass, entry)

    # Listen for options changes to reconfigure the purger
    async def _options_updated(hass_: HomeAssistant, updated_entry: ConfigEntry):
        _LOGGER.debug("WTime options updated; reconfiguring autopurger")
        _start_or_stop_autopurger(hass, updated_entry)

    bucket["update_unsub"] = entry.add_update_listener(_options_updated)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    # Stop purger
    bucket = _get_entry_bucket(hass, entry.entry_id)
    if bucket.get("purge_unsub"):
        bucket["purge_unsub"]()
        bucket["purge_unsub"] = None

    if bucket.get("update_unsub"):
        bucket["update_unsub"]()
        bucket["update_unsub"] = None

    ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    # Cleanup container
    hass.data.get(DOMAIN, {}).pop(entry.entry_id, None)
    if not hass.data.get(DOMAIN):
        hass.data.pop(DOMAIN, None)

    return ok


def async_get_options_flow(config_entry: ConfigEntry):
    from .config_flow import WTimeOptionsFlow
    return WTimeOptionsFlow(config_entry)


# ---------- Auto-purger ----------
def _start_or_stop_autopurger(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Start or stop the recorder purge scheduler according to options."""
    bucket = _get_entry_bucket(hass, entry.entry_id)

    # Cancel existing schedule
    if bucket.get("purge_unsub"):
        bucket["purge_unsub"]()
        bucket["purge_unsub"] = None

    enabled: bool = entry.options.get(CONF_AUTOPURGE_ENABLED, True)
    entity_ids: list[str] = entry.options.get(CONF_AUTOPURGE_ENTITY_IDS, DEFAULT_AUTOPURGE_ENTITY_IDS)
    interval_s: int = int(entry.options.get(CONF_AUTOPURGE_INTERVAL, DEFAULT_AUTOPURGE_INTERVAL))

    if not enabled or not entity_ids or interval_s < 15:
        _LOGGER.debug("WTime autopurger disabled or misconfigured (enabled=%s, entities=%d, interval=%ss)",
                      enabled, len(entity_ids), interval_s)
        return

    interval = timedelta(seconds=interval_s)

    async def _purge_tick(_now):
        # Only run if the service exists (otherwise spammy)
        if not hass.services.has_service("recorder", "purge_entities"):
            _LOGGER.debug("recorder.purge_entities service not found; skipping this cycle")
            return
        try:
            await hass.services.async_call(
                "recorder",
                "purge_entities",
                {"entity_ids": entity_ids, "repack": False},
                blocking=False,
            )
            _LOGGER.debug("Requested purge for %d entities", len(entity_ids))
        except Exception as err:
            _LOGGER.debug("recorder.purge_entities failed: %s", err)

    # Schedule periodic purge
    bucket["purge_unsub"] = async_track_time_interval(hass, _purge_tick, interval)
    # Fire once shortly after startup
    hass.async_create_task(_purge_tick(None))
