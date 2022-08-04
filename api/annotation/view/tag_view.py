
from flask import Blueprint
from api.annotation.general.module_constants import REST_API_V1_BASE_URL
from api.annotation.service.tag.tag_service import TagService
from ipsum.view.crud_view import CRUDView
from ipsum.view.ipsum_view import IpsumView


tag_view_name = TagService.NAME
tag_blueprint = Blueprint(tag_view_name, __name__)

class TagView(IpsumView):

    route_prefix = REST_API_V1_BASE_URL

    route_base = tag_view_name

    def __init__(self) -> None:

        super().__init__(service=TagService())

TagView.register(tag_blueprint)