# Sample configuration
Set up the sensor using the configuration file (```configuration.yaml```).
```
  - platform: sjofartsverket_viva
    name: Vind
    region: 114
    scan_interval: 60
  - platform: template
    sensors:
      vind2:
        friendly_name: "Byvind"
        entity_id: sensor.vind
        unit_of_measurement: 'm/s'
        value_template: "{{ state_attr('sensor.vind', 'Wind max') }}"
```
The region can be found at Sjöfartsverket (https://geokatalog.sjofartsverket.se/kartvisarefyren/), select a station and view the "stationsid" parameter. Some examples: Vinga/Göteborg is 114 and Gubben/Sundsvall is 153. scan_interval is the number of seconds between requests to ViVa, please do not poll too often. The selected station must have a value for "Medelvind", otherwise the component will not receive any data.
