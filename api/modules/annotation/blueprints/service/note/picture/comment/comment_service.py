
from unicodedata import name
from api.modules.annotation.blueprints.data.dao.picture_dao import PictureDAO
from api.modules.annotation.blueprints.service.note.picture.picture_service import PictureService
from arq.service.detail_crud_service import DetailCRUDService
from api.modules.annotation.blueprints.data.model.comment import Comment
from api.modules.annotation.blueprints.data.dao.comment_dao import CommentDAO
from arq.util.service.collection_tree import CollectionItem, CollectionTree
from api.modules.annotation.blueprints.service.note.picture.comment.comment_validator import CommentValidator

class CommentService(DetailCRUDService):

    NAME = 'comments'

    fields_inserted_by_default = [Comment.parent_field]   

    def __init__(self) -> None:
        comment_dao = CommentDAO()
        picture_dao = PictureDAO()

        collection_tree = CollectionTree(
            parent=CollectionItem(
                name=PictureService.NAME,
                parent_field=picture_dao.model.parent_field,
                dao=picture_dao,
                id=None,
                field=comment_dao.model.parent_field
            ),
            child=CollectionItem(
                name=self.NAME,
                parent_field=comment_dao.model.parent_field,
                dao=comment_dao,
                id=None,
                field='id'
            )
        )

        super().__init__(
            dao=collection_tree.child.dao, 
            validator=CommentValidator(
                dao=collection_tree.child.dao,
                parent_dao=collection_tree.parent.dao
            ), 
            collection_tree=collection_tree
        )
