from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.selector import (
    SelectSelector, SelectSelectorConfig, SelectSelectorMode, SelectOptionDict,
    NumberSelector, NumberSelectorConfig, BooleanSelector,
)

from .const import (
    DOMAIN,
    CONF_AUTOPURGE_ENABLED,
    CONF_AUTOPURGE_ENTITY_IDS,
    CONF_AUTOPURGE_INTERVAL,
    DEFAULT_AUTOPURGE_INTERVAL,
    DEFAULT_AUTOPURGE_ENTITY_IDS,
)


class WTimeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle config flow for WTime."""
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")
        # No questions; creating the entry triggers HA's “Device created” screen.
        return self.async_create_entry(title="WTime", data={})


# -------- Options Flow: choose entities to auto-purge + interval --------
class WTimeOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        hass: HomeAssistant = self.hass
        ent_reg = er.async_get(hass)

        # Collect *this* integration's sensor/binary_sensor entities so the list is clean
        wtime_entities = [
            e for e in ent_reg.entities.values()
            if e.config_entry_id == self.config_entry.entry_id
            and e.domain in ("sensor", "binary_sensor")
        ]
        wtime_entities.sort(key=lambda x: x.entity_id)

        # Build nice dropdown labels with current state preview
        options = []
        for e in wtime_entities:
            st = hass.states.get(e.entity_id)
            state_txt = st.state if st is not None else "unavailable"
            options.append(SelectOptionDict(label=f"{e.entity_id} — {state_txt}", value=e.entity_id))

        # Pull existing options or use defaults
        cur_enabled = self.config_entry.options.get(CONF_AUTOPURGE_ENABLED, True)
        cur_entities = self.config_entry.options.get(CONF_AUTOPURGE_ENTITY_IDS, DEFAULT_AUTOPURGE_ENTITY_IDS)
        cur_interval = self.config_entry.options.get(CONF_AUTOPURGE_INTERVAL, DEFAULT_AUTOPURGE_INTERVAL)

        # Ensure defaults are visible in dropdown: if a default entity isn't found
        # (e.g., renamed), it simply won't appear; that's OK—the user can reselect.
        if user_input is None:
            schema = vol.Schema({
                vol.Required(CONF_AUTOPURGE_ENABLED, default=cur_enabled): BooleanSelector(),
                vol.Optional(
                    CONF_AUTOPURGE_ENTITY_IDS,
                    default=[e for e in cur_entities if any(o.value == e for o in options)]
                ): SelectSelector(
                    SelectSelectorConfig(
                        options=options,
                        multiple=True,
                        mode=SelectSelectorMode.DROPDOWN,
                        custom_value=False,  # restrict to known entities
                    )
                ),
                vol.Required(
                    CONF_AUTOPURGE_INTERVAL,
                    default=cur_interval
                ): NumberSelector(NumberSelectorConfig(min=15, max=86400, step=1, mode="box")),
            })
            return self.async_show_form(step_id="init", data_schema=schema)

        # Save options
        enabled = bool(user_input.get(CONF_AUTOPURGE_ENABLED, True))
        entities = list(user_input.get(CONF_AUTOPURGE_ENTITY_IDS, []))
        interval = int(user_input.get(CONF_AUTOPURGE_INTERVAL, DEFAULT_AUTOPURGE_INTERVAL))

        return self.async_create_entry(
            title="WTime Options",
            data={
                CONF_AUTOPURGE_ENABLED: enabled,
                CONF_AUTOPURGE_ENTITY_IDS: entities,
                CONF_AUTOPURGE_INTERVAL: interval,
            },
        )
