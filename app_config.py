import logging
import configparser

logger = logging.getLogger("config")

config = configparser.ConfigParser()

config.read('config.ini')
LOG = config.get('app', 'LOG')

API_TOKEN = config.get('app', 'API_TOKEN')
if not API_TOKEN:
    raise ValueError('No API_TOKEN specified! Please specify a valid api token in the config.ini file.')

LOCATION = config.get('app', 'LOCATION')
if not LOCATION:
    raise IOError('No path to folder to track is specified! Please specify the absolute path to the folder to track.')

REMOTE_LOCATION = config.get('app', 'REMOTE_LOCATION')

PERIOD = config.get('app', 'PERIOD')

