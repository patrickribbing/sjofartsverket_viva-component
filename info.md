# Usage
Set up the sensor using yaml in the configuration file (```configuration.yaml```).
```
sensor vind:
  platform: viva
  name: Vind
  region: 114
  scan_interval: 60
```
The region can be found at Sjöfartsverket (https://geokatalog.sjofartsverket.se/kartvisarefyren/), select a station and view the "stationsid" parameter. Some examples: Vinga/Göteborg is 114 and Gubben/Sundsvall is 153. scan_interval is the number of seconds between requests to ViVa, please do not poll too often. The selected station must have a value for "Medelvind", otherwise the component will not receive any data.
