
import os
from flask import Flask
from flask_mongoengine import MongoEngine

db = MongoEngine()

def set_database_config(flask_app: Flask):
    MONGODB_HOST = get_database_config()

    flask_app.config.update(**{"MONGODB_HOST": MONGODB_HOST})

def get_database_config():
    MONGODB_HOST = None

    if not _is_test_enviroment():
        print('NOT _is_test_enviroment ')
        MONGODB_HOST = _get_default_database_config()
    
    else:
        MONGODB_HOST = _get_test_database_config()
    
    return MONGODB_HOST

# TODO Criar arquivo para constantes das variavies de ambiente ARQ
# TODO Criar facilitador para lidar com variavies de ambiente ou arquivos de config

def _is_test_enviroment():
    TEST_ENVIROMENT = 'TEST_ENVIROMENT'
    
    if TEST_ENVIROMENT in os.environ:
        return str(os.environ[TEST_ENVIROMENT]) == '1'
    
    return False


def _get_default_database_config():
    MONGODB_USER = os.environ['MONGODB_USER']
    MONGODB_PASSWORD = os.environ['MONGODB_PASSWORD']
    MONGODB_DATABASE = os.environ['MONGODB_DATABASE']
    MONGODB_ATLAS_PREFIX = os.environ['MONGODB_ATLAS_PREFIX']
    MONGODB_URL_OPTIONS = os.environ['MONGODB_URL_OPTIONS']

    MONGODB_HOST = 'mongodb+srv://'+MONGODB_USER+':'+MONGODB_PASSWORD+'@'+MONGODB_ATLAS_PREFIX+'/'+MONGODB_DATABASE+'?'+MONGODB_URL_OPTIONS
    return MONGODB_HOST

def _get_test_database_config():
    return "mongodb+srv://user:senha@anotacoes-cluster.jwtdf.mongodb.net/anotacoes-integration-test?retryWrites=true&w=majority"