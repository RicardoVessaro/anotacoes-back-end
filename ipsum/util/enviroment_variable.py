
import os

MONGODB_USER = 'MONGODB_USER'
MONGODB_PASSWORD = 'MONGODB_PASSWORD'
MONGODB_DATABASE = 'MONGODB_DATABASE'
MONGODB_ATLAS_PREFIX = 'MONGODB_ATLAS_PREFIX'
MONGODB_URL_OPTIONS = 'MONGODB_URL_OPTIONS'

TEST_ENVIROMENT = 'TEST_ENVIROMENT'

INTEGRATION_TEST_HOST = 'INTEGRATION_TEST_HOST'
INTEGRATION_TEST_PORT = 'INTEGRATION_TEST_PORT' 

TEST_MONGODB_USER = 'TEST_MONGODB_USER'
TEST_MONGODB_PASSWORD = 'TEST_MONGODB_PASSWORD'
TEST_MONGODB_ATLAS_PREFIX = 'TEST_MONGODB_ATLAS_PREFIX'
TEST_MONGODB_DATABASE = 'TEST_MONGODB_DATABASE'
TEST_MONGODB_URL_OPTIONS = 'TEST_MONGODB_URL_OPTIONS'

_MONGODB_ATLAS_SERVER_PREFIX = 'mongodb+srv://'

def get_enviroment_variable(enviroment_variable_name):
    return os.environ[enviroment_variable_name]
        
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

def get_test_database_url():
    
    test_mongodb_user = get_enviroment_variable(TEST_MONGODB_USER)
    test_mongodb_password = get_enviroment_variable(TEST_MONGODB_PASSWORD)
    test_mongodb_atlas_prefix = get_enviroment_variable(TEST_MONGODB_ATLAS_PREFIX)
    test_mongodb_database = get_enviroment_variable(TEST_MONGODB_DATABASE)
    test_mongodb_url_options = get_enviroment_variable(TEST_MONGODB_URL_OPTIONS)
    
    return f'{_MONGODB_ATLAS_SERVER_PREFIX}{test_mongodb_user}:{test_mongodb_password}@{test_mongodb_atlas_prefix}/{test_mongodb_database}?{test_mongodb_url_options}'

def is_test_enviroment():
    if TEST_ENVIROMENT in os.environ:
        return str(os.environ[TEST_ENVIROMENT]) == '1'
    
    return False
