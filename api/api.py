
import os
from flask import Flask
from api.db import db

def create_flask_app():
    
    api = Flask(__name__)

    _set_database_config(api)

    db.init_app(api)

    return api

def _set_database_config(flask_app):
    MONGODB_USER = os.environ['MONGODB_USER']
    MONGODB_PASSWORD = os.environ['MONGODB_PASSWORD']
    MONGODB_DATABASE = os.environ['MONGODB_DATABASE']
    MONGODB_ATLAS_PREFIX = os.environ['MONGODB_ATLAS_PREFIX']
    MONGODB_URL_OPTIONS = os.environ['MONGODB_URL_OPTIONS']

    MONGODB_HOST = 'mongodb+srv://'+MONGODB_USER+':'+MONGODB_PASSWORD+'@'+MONGODB_ATLAS_PREFIX+'/'+MONGODB_DATABASE+'?'+MONGODB_URL_OPTIONS

    flask_app.config.update(**{"MONGODB_HOST": MONGODB_HOST})
