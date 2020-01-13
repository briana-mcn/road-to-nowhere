import os 

from config import config

run_mode = os.environ.get('RUN_MODE', 'dev')
config_settings = config.ConfigDev

if run_mode == 'prod':
    config_settings = config.ConfigProd

elif run_mode == 'test':
    config_settings = config.ConfigTest
