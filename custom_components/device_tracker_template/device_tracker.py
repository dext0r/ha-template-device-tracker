from typing import Any

from homeassistant.components.device_tracker.const import ATTR_SOURCE_TYPE, SourceType
from homeassistant.components.template.const import CONF_ATTRIBUTES, CONF_PICTURE
from homeassistant.components.template.template_entity import TemplateEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_ICON, CONF_LOCATION, CONF_UNIQUE_ID, STATE_HOME, STATE_NOT_HOME
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.template import Template
from homeassistant.helpers.typing import ConfigType

from . import CONF_SOURCE_TYPE, DOMAIN


async def async_setup_entry(hass: HomeAssistant, _: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    tracker_configs: list[ConfigType] = hass.data[DOMAIN]
    async_add_entities([DeviceTrackerTemplateEntity(hass, config) for config in tracker_configs])


class DeviceTrackerTemplateEntity(TemplateEntity):
    _attr_should_poll = False

    def __init__(self, hass: HomeAssistant, config: ConfigType):
        super().__init__(
            hass,
            config=config,
            icon_template=config.get(CONF_ICON),
            entity_picture_template=config.get(CONF_PICTURE),
            attribute_templates=config.get(CONF_ATTRIBUTES),
            unique_id=config.get(CONF_UNIQUE_ID),
        )

        self._template: Template = config[CONF_LOCATION]
        self._source_type_template: Template | None = config.get(CONF_SOURCE_TYPE)
        self._attr_extra_state_attributes[ATTR_SOURCE_TYPE] = SourceType.GPS

    @callback
    def _async_setup_templates(self) -> None:
        super()._async_setup_templates()

        self.add_template_attribute(
            "_attr_state", self._template, None, self._update_state, none_on_template_error=True
        )

        if self._source_type_template:
            self.add_template_attribute("_attr_source_type", self._source_type_template, None, self._update_source_type)

    @callback
    def _update_state(self, result: Any) -> None:
        if isinstance(result, bool):
            self._attr_state = STATE_HOME if result else STATE_NOT_HOME
            return

        self._attr_state = result

    @callback
    def _update_source_type(self, result: Any) -> None:
        self._attr_extra_state_attributes[ATTR_SOURCE_TYPE] = result if isinstance(result, str) else SourceType.GPS
