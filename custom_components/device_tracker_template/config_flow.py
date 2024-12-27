from typing import Any

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult

from . import DOMAIN


class DeviceTrackerTemplateConfigFlow(ConfigFlow, domain=DOMAIN):

    VERSION = 1

    async def async_step_import(self, import_data: dict[str, Any]) -> ConfigFlowResult:
        return self.async_create_entry(title="configuration.yaml", data=import_data)
