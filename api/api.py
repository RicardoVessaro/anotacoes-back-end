
import os

from flask import Flask
from api.db import db, set_database_config
from api.modules.core.blueprints.view import note_view, tag_view
from arq.exception.arq_exception import ArqException
from arq.exception.arq_exception import error_handler
from arq.service.enum.arq_enum import save_enums

# TODO Criar ARQ Logger

def create_flask_app():
    
    api = Flask(__name__)
    api.register_error_handler(ArqException, error_handler)

    set_database_config(api)

    _register_blueprint(api)

    db.init_app(api)

    save_enums()

    return api

# TODO Criar decorator para blueprints
def _register_blueprint(flask_app: Flask):
    _register_core_blueprint(flask_app)


def _register_core_blueprint(flask_app: Flask):
    flask_app.register_blueprint(note_view.note_blueprint)
    flask_app.register_blueprint(tag_view.tag_blueprint)





