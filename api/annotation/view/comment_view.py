

from flask import Blueprint
from api.annotation.general.module_constants import REST_API_V1_BASE_URL
from api.annotation.service.note.picture.picture_service import PictureService
from ipsum.view.detail_crud_view import DetailCRUDView
from api.annotation.service.note.picture.comment.comment_service import CommentService
from api.annotation.data.model.comment import Comment

comment_view_name = CommentService.NAME
comment_blueprint = Blueprint(comment_view_name, __name__)

class CommentView(DetailCRUDView):

    route_prefix = f'{REST_API_V1_BASE_URL}{PictureService.NAME}/<{Comment.parent_field}>/'

    route_base = comment_view_name

    def __init__(self) -> None:
        
        super().__init__(
            service=CommentService()
        )

CommentView.register(comment_blueprint)
