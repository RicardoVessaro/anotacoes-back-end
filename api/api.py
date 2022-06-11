
import os

from flask import Flask
from api.db import db, set_database_config
from api.annotation.view import note_view, tag_view, mood_view, picture_view, comment_view, link_view
from ipsum.exception.ipsum_exception import IpsumException
from ipsum.exception.ipsum_exception import error_handler
from ipsum.ipsum_flask.ipsum_flask import IpsumFlask
from ipsum.service.enum.ipsum_enum import save_enums

def create_flask_app():
    
    api = IpsumFlask(__name__)
    api.register_error_handler(IpsumException, error_handler)

    set_database_config(api)

    _register_blueprint(api)

    db.init_app(api)

    save_enums()

    return api

def _register_blueprint(flask_app: Flask):
    flask_app.register_blueprint(tag_view.tag_blueprint)
    flask_app.register_blueprint(mood_view.mood_blueprint)
    flask_app.register_blueprint(note_view.note_blueprint)
    flask_app.register_blueprint(picture_view.picture_blueprint)
    flask_app.register_blueprint(comment_view.comment_blueprint)
    flask_app.register_blueprint(link_view.link_blueprint)





