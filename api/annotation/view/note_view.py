
from flask import Blueprint
from api.annotation.data.model.link import Link
from api.annotation.data.model.picture import Picture
from api.annotation.service.note.note_service import NoteService
from api.annotation.general.module_constants import REST_API_V1_BASE_URL
from api.annotation.view.link_view import LinkView, link_view_name
from api.annotation.view.picture_view import PictureView, picture_view_name
from ipsum.view.crud_view import CRUDView, CollectionView

note_view_name = NoteService.NAME
note_blueprint = Blueprint(note_view_name, __name__)

class NoteView(CRUDView):

    route_prefix = REST_API_V1_BASE_URL

    route_base = note_view_name

    def __init__(self) -> None:
        child_collections = [
            CollectionView(PictureView, Picture.parent_field, picture_view_name),
            CollectionView(LinkView, Link.parent_field, link_view_name)
        ]

        super().__init__(
            service=NoteService(),
            child_collections=child_collections
        )

NoteView.register(note_blueprint)