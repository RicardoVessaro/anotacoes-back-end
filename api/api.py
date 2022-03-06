
import os

from flask import Flask
from api.db import db
from api.modules.core.blueprints.view import note_view
from arq.exception.arq_exception import ArqException
from arq.exception.arq_exception import error_handler
def create_flask_app():
    
    api = Flask(__name__)
    api.register_error_handler(ArqException, error_handler)

    _set_database_config(api)

    _register_blueprint(api)

    db.init_app(api)

    return api

def _register_blueprint(flask_app: Flask):
    _register_core_blueprint(flask_app)


def _register_core_blueprint(flask_app: Flask):
    flask_app.register_blueprint(note_view.note_blueprint)


def _set_database_config(flask_app: Flask):
    MONGODB_USER = os.environ['MONGODB_USER']
    MONGODB_PASSWORD = os.environ['MONGODB_PASSWORD']
    MONGODB_DATABASE = os.environ['MONGODB_DATABASE']
    MONGODB_ATLAS_PREFIX = os.environ['MONGODB_ATLAS_PREFIX']
    MONGODB_URL_OPTIONS = os.environ['MONGODB_URL_OPTIONS']

    MONGODB_HOST = 'mongodb+srv://'+MONGODB_USER+':'+MONGODB_PASSWORD+'@'+MONGODB_ATLAS_PREFIX+'/'+MONGODB_DATABASE+'?'+MONGODB_URL_OPTIONS

    flask_app.config.update(**{"MONGODB_HOST": MONGODB_HOST})


