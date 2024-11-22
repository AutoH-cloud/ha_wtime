from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN

class WtimeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Wtime."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            return self.async_create_entry(title="Wtime", data={})

        return self.async_show_form(step_id="user")

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return WtimeOptionsFlowHandler(config_entry)

class WtimeOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle an options flow for Wtime."""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(step_id="init", data_schema=None)
