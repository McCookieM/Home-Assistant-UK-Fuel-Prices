"""Define constants used in uk_fuel_prices."""

import logging

DOMAIN = "uk_fuel_prices"

CONF_RETAILERS = "retailers"
CONF_FUEL_TYPE = "fuel_type"
CONF_UPDATE_FREQUENCY = "update_frequency"

SENSOR_PREFIX = "UK Fuel Price "

GOV_LIST = "https://www.gov.uk/guidance/access-fuel-price-data"
TABLE_XPATH = "/html/body/div[3]/main/div[4]/div[1]/div/div[2]/div/table"

_LOGGER = logging.getLogger(__name__)
