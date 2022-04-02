from flask import Blueprint
from api.modules.core.blueprints.service.tag.tag_service import TagService
from arq.view.crud_view import CRUDView


tag_view_name = 'tag'
tag_blueprint = Blueprint(tag_view_name, __name__)

class TagView(CRUDView):

    def __init__(self) -> None:

        super().__init__(service=TagService())

TagView.register(tag_blueprint)