
import os

LOGGER_LEVEL = 'LOGGER_LEVEL'

MONGODB_USER = 'MONGODB_USER'
MONGODB_PASSWORD = 'MONGODB_PASSWORD'
MONGODB_DATABASE = 'MONGODB_DATABASE'
MONGODB_ATLAS_PREFIX = 'MONGODB_ATLAS_PREFIX'
MONGODB_URL_OPTIONS = 'MONGODB_URL_OPTIONS'

INTEGRATION_TEST_HOST = 'INTEGRATION_TEST_HOST'
INTEGRATION_TEST_PORT = 'INTEGRATION_TEST_PORT' 

_MONGODB_ATLAS_SERVER_PREFIX = 'mongodb+srv://'

config_variables = {}

def set_config_variables(app_config):
    global config_variables

    config_variables = app_config
    

def get_enviroment_variable(enviroment_variable_name):

    if enviroment_variable_name in os.environ:
        return os.environ[enviroment_variable_name]

    elif enviroment_variable_name in config_variables:
        return config_variables[enviroment_variable_name]
    
    return None
        
def get_api_url():

    integration_test_host = get_enviroment_variable(INTEGRATION_TEST_HOST)
    integration_test_port = get_enviroment_variable(INTEGRATION_TEST_PORT)

    return f'{integration_test_host}:{integration_test_port}'

def get_database_url():

    mongodb_user = get_enviroment_variable(MONGODB_USER)
    mongodb_password = get_enviroment_variable(MONGODB_PASSWORD)
    mongodb_atlas_prefix = get_enviroment_variable(MONGODB_ATLAS_PREFIX)
    mongodb_database = get_enviroment_variable(MONGODB_DATABASE)
    mongodb_url_options = get_enviroment_variable(MONGODB_URL_OPTIONS)
    
    return f'{_MONGODB_ATLAS_SERVER_PREFIX}{mongodb_user}:{mongodb_password}@{mongodb_atlas_prefix}/{mongodb_database}?{mongodb_url_options}'
