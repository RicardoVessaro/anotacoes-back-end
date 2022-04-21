
import os
from flask import Flask
from flask_mongoengine import MongoEngine

from arq.util.enviroment_variable import get_database_url, get_test_database_url, is_test_enviroment

db = MongoEngine()

def set_database_config(flask_app: Flask):
    MONGODB_HOST = get_database_config()

    flask_app.config.update(**{"MONGODB_HOST": MONGODB_HOST})

def get_database_config():
    MONGODB_HOST = None

    if not is_test_enviroment():
        MONGODB_HOST = get_database_url()
    
    else:
        MONGODB_HOST = get_test_database_url()
    
    return MONGODB_HOST
