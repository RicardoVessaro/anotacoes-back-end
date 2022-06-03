
from unicodedata import name
from api.annotation.data.dao.picture_dao import PictureDAO
from api.annotation.service.note.picture.picture_service import PictureService
from ipsum.service.detail_crud_service import DetailCRUDService
from api.annotation.data.model.comment import Comment
from api.annotation.data.dao.comment_dao import CommentDAO
from ipsum.util.service.collection_tree import CollectionItem, CollectionTree
from api.annotation.service.note.picture.comment.comment_validator import CommentValidator

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
