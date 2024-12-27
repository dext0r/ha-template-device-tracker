from typing import Any

from homeassistant.components.template.const import CONF_ATTRIBUTES, CONF_PICTURE
from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.const import CONF_ICON, CONF_LOCATION, CONF_NAME, CONF_UNIQUE_ID, SERVICE_RELOAD
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.reload import async_integration_yaml_config
from homeassistant.helpers.service import async_register_admin_service
from homeassistant.helpers.typing import ConfigType
import voluptuous as vol

from .const import CONF_SOURCE_TYPE, DOMAIN, PLATFORMS

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: [
            {
                vol.Required(CONF_NAME): cv.template,
                vol.Required(CONF_LOCATION): cv.template,
                vol.Optional(CONF_SOURCE_TYPE): cv.template,
                vol.Optional(CONF_UNIQUE_ID): cv.string,
                vol.Optional(CONF_ICON): cv.template,
                vol.Optional(CONF_PICTURE): cv.template,
                vol.Optional(CONF_ATTRIBUTES): vol.Schema({cv.string: cv.template}),
            }
        ]
    },
    extra=vol.ALLOW_EXTRA,
)


async def async_setup(hass: HomeAssistant, yaml_config: ConfigType) -> bool:
    hass.data[DOMAIN] = yaml_config.get(DOMAIN, [])

    async def _reload_service_handler(_: Any) -> None:
        if reload_config := await async_integration_yaml_config(hass, DOMAIN):
            hass.data[DOMAIN] = reload_config.get(DOMAIN, {})

        for entry in hass.config_entries.async_entries(DOMAIN):
            await hass.config_entries.async_reload(entry.entry_id)

    async_register_admin_service(hass, DOMAIN, SERVICE_RELOAD, _reload_service_handler)

    if not hass.config_entries.async_entries(DOMAIN):
        hass.async_create_task(
            hass.config_entries.flow.async_init(DOMAIN, context={"source": SOURCE_IMPORT}, data={}),
        )

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
