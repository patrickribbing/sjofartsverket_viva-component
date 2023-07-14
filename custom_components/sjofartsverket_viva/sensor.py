# -*- coding: utf-8 -*-

import logging
import json
import requests
from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (ATTR_ATTRIBUTION, CONF_OFFSET, CONF_NAME, CONF_ID, CONF_SCAN_INTERVAL, CONF_REGION)
import homeassistant.helpers.config_validation as cv
import homeassistant.util.dt as dt_util
import voluptuous

_LOGGER = logging.getLogger(__name__)

DEFAULT_REGION = 76
DEFAULT_NAME = 'ViVa data'
DEFAULT_SCAN_INTERVAL = 60

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    voluptuous.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    voluptuous.Optional(CONF_ID, default=''): cv.string,
    voluptuous.Optional(CONF_REGION, default=DEFAULT_REGION): cv.positive_int,
    voluptuous.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): cv.time_period,
})

def setup_platform(hass, config, add_devices, discovery_info=None):
    station_id = config.get(CONF_REGION)
    name = config.get(CONF_NAME)
    _LOGGER.info('ViVa setup. Station=' + str(station_id))
    add_devices([ViVa(name, station_id)])

class ViVa(Entity):
    def __init__(self, name, station_id):
        self._state = None
        self._name = name
        self._station_id = station_id
        self._direction_str = ''
        self._station_name = ''
        self._water_temp = ''
        self._wind_max = ''
        self._wind_heading = 0
        self._water_level = ''

        # fetch data
        self.update()

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def unit_of_measurement(self):
        return 'm/s'

    @property
    def extra_state_attributes(self):
        return {
            'Station id': self._station_id,
            'Station': self._station_name,
            'Wind': self._state,
            'Wind max': self._wind_max,
            'Direction': self._direction_str,
            'Wind heading': self._wind_heading,
            'Water temperature': self._water_temp,
            'Water level': self._water_level,
            ATTR_ATTRIBUTION: 'For details, see https://www.sjofartsverket.se/sv/tjanster/vind--och-vatteninformation-viva/'
        }

    def update(self):
        try:
            viva_request = requests.get('https://services.viva.sjofartsverket.se:8080/output/vivaoutputservice.svc/vivastation/' + str(self._station_id))
            data = json.loads(viva_request.text)
            self._station_name = data['GetSingleStationResult']['Name']
            for sample in data['GetSingleStationResult']['Samples']:
                if sample['Name'] == 'Medelvind':
                    wind = sample['Value'].split(' ', 1)
                    self._state = wind[1]
                    self._direction_str = wind[0]
                    self._wind_heading = sample['Heading']
                if sample['Name'] == 'Byvind':
                    wind_max = sample['Value'].split(' ', 1)
                    self._wind_max = wind_max[1]
                if sample['Name'] == 'Vattentemp':
                    self._water_temp = sample['Value']
                if sample['Name'] == 'Vattenstånd':
                    self._water_level = sample['Value']
            _LOGGER.debug('Fetching ViVa data from station=' + self._station_name + ' (' + str(self._station_id) + '), wind=' + str(self._state) + ', direction=' + self._direction_str + ', heading=' + str(self._wind_heading))
        except:
            _LOGGER.critical('Exception fetching ViVa data from station=' + str(self._station_id))
            self._station_name = ''
            self._state = 0
            self._direction_str = ''
            self._water_temp = ''
            self._wind_max = ''
            self._wind_heading = 0
            self._water_level = ''
