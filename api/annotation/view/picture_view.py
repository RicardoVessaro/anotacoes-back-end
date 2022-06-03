
from flask import Blueprint
from api.annotation.general.module_constants import REST_API_V1_BASE_URL
from api.annotation.service.note.note_service import NoteService
from ipsum.view.detail_crud_view import DetailCRUDView
from api.annotation.service.note.picture.picture_service import PictureService
from api.annotation.data.model.picture import Picture

picture_view_name = PictureService.NAME
picture_blueprint = Blueprint(picture_view_name, __name__)

class PictureView(DetailCRUDView):

    route_prefix = f'{REST_API_V1_BASE_URL}{NoteService.NAME}/<{Picture.parent_field}>/'

    route_base = picture_view_name

    def __init__(self) -> None:
        super().__init__(service=PictureService())

PictureView.register(picture_blueprint)