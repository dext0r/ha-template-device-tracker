# Template Device Tracker

Home Assistant custom component that creates the Device Tracker entity based on templates.

## Configuration

All configuration variables are optional, except `name` and `location`.

| Name        | Type                                                                                        | Description                                                                                                                                                                             |
| ----------- | ------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| name        | `string`                                                                                    | The name of the device tracker.                                                                                                                                                         |
| location    | [`template`](https://www.home-assistant.io/docs/configuration/templating)                   | Defines a template to get the state of the device tracker. The state is `home` if the template evaluates as `True`, `not_home` if `False`, otherwise template value will be used as is. |
| source_type | [`template`](https://www.home-assistant.io/docs/configuration/templating)                   | Defines a template to get the `source_type` attribute of the device tracker.                                                                                                            |
| unique_id   | `string`                                                                                    | The [unique ID](https://developers.home-assistant.io/docs/entity_registry_index/#unique-id) of the device tracker.                                                                      |
| icon        | [`template`](https://www.home-assistant.io/docs/configuration/templating)                   | Defines a template for the icon of the device tracker.                                                                                                                                  |
| picture     | [`template`](https://www.home-assistant.io/docs/configuration/templating)                   | Defines a template for the entity picture of the device tracker.                                                                                                                        |
| attributes  | map[`attribute`: [`template`](https://www.home-assistant.io/docs/configuration/templating)] | Defines templates for attributes of the device tracker.                                                                                                                                 |

## Example Configuration

```yaml
device_tracker_template:
  - name: ESPHome Presence
    unique_id: esphome_presence
    location: "{{ states('binary_sensor.esphome_ble_presence') }}" # home or not_home
    source_type: bluetooth_le

  - name: Fake GPS Presence
    location: "{{ 'Near Home' if states('binary_sensor.some_binary_sensor') else False }}"  # Near Home or not_home
    source_type: gps
```
