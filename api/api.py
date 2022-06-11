
import os

from api.db import db
from api.annotation.view import note_view, tag_view, mood_view, picture_view, comment_view, link_view
from ipsum.ipsum_flask.factory import IpsumFlaskFactory

def create_flask_app():

    blueprints = [
        note_view.note_blueprint, 
        tag_view.tag_blueprint,
        mood_view.mood_blueprint,
        picture_view.picture_blueprint,
        comment_view.comment_blueprint,
        link_view.link_blueprint
    ]

    api = IpsumFlaskFactory(
        name=__name__,
        database_object=db,
        blueprints=blueprints
    ).app

    return api
    