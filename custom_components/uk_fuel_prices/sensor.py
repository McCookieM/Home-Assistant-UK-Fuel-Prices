"""
Sensor component for UK Fuel Prices
Author: McCookieM
"""
import requests
import voluptuous as vol
from datetime import datetime, date, timedelta
import urllib.error
from urllib.parse import urljoin, urlparse
from typing import Any, Callable, Dict, Optional

from homeassistant.components.sensor import PLATFORM_SCHEMA, SensorDeviceClass
import homeassistant.helpers.config_validation as cv
from homeassistant.util import Throttle
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.typing import (
    HomeAssistantType,
    ConfigType,
    DiscoveryInfoType,
)

from .const import (
    _LOGGER,
    DOMAIN,
    SENSOR_PREFIX,
    GOV_LIST,
    TABLE_XPATH,
    CONF_RETAILERS,
    CONF_FUEL_TYPE,
    CONF_UPDATE_FREQUENCY,
)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_RETAILERS): cv.ensure_list,
        vol.Optional(CONF_FUEL_TYPE): cv.string,
        vol.Optional(CONF_UPDATE_FREQUENCY, default=24): cv.string,
    }
)

async def async_setup_platform(
    hass: HomeAssistantType,
    config: ConfigType,
    async_add_entities: Callable,
    discovery_info: Optional[DiscoveryInfoType]=None,
) -> None:
    """Set up the sensor platform."""
    _LOGGER.debug("Setting up UK Fuel Prices sensor platform")

    SCAN_INTERVAL = timedelta(hours=(int(config[CONF_UPDATE_FREQUENCY])))
    fuel_type = config[CONF_FUEL_TYPE]

    sensors = [
        UKFuelPricesSensor(
            retailer,
            fuel_type
        )
        for retailer in config[CONF_RETAILERS]
    ]

    async_add_entities(sensors, update_before_add=True)
        
class UKFuelPricesSensor(Entity):
    """Representation of a UK Fuel Prices sensor."""
    
    def __init__(self, retailer:str, fuel_type:str):
        super().__init__()
        self.data = None
        self.retailer = retailer.lower().strip()
        self.fuel_type = fuel_type.lower().strip()
        self._attr_device_class = SensorDeviceClass.MONETARY
        self._name = (SENSOR_PREFIX + retailer + " " + fuel_type)
        self._icon = "mdi:gas-station"
        self._state = None
        self._available = True
        self._last_update = None
        self._latitude = None
        self._longitude = None
        self._unit_of_measurement = "£"

    @property
    def name(self) -> str:
        return self._name

    @property
    def icon(self) -> str:
        return self._icon

    @property
    def state(self) -> Optional[str]:
        return self._state

    @property
    def unique_id(self) -> str:
        return f"{DOMAIN}-{self.retailer}-{self.fuel_type}"
    
    @property
    def unit_of_measurement(self) -> str:
        return self._unit_of_measurement
    
    @property
    def available(self) -> bool:
        return self._available

    @property
    def device_state_attributes(self):
        return {
            ATTR_LAST_UPDATE: self._last_update,
            ATTR_LATITUDE: self._latitude,
            ATTR_LONGITUDE: self._longitude
        }
    
    async def async_update(self):
        try:
            url = (
                GOV_LIST
            )
            # sending get request
            r = requests.get(url=url)
            # get table from page
            # loop table and get retailer data
            # keep required fuel data
            # extracting response json

            if self.data:
                # Set the values of the sensor
                self._last_update = datetime.today().strftime("%d-%m-%Y %H:%M") # Get it
                # set the attributes of the sensor
                self._latitude = None # Get it
                self._longitude = None # Get it

                # Set state and availability
                self._state = float(self.data)
                self._available = True
            else:
                raise ValueError()
        except ValueError:
            self._state = None
            self._last_update = datetime.today().strftime("%d-%m-%Y %H:%M")
            self._latitude = None
            self._longitude = None
        except (error):
            self._available = False
            _LOGGER.exception("Error retrieving data")
