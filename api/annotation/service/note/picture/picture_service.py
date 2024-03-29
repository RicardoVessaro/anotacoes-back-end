
from api.annotation.data.dao.note_dao import NoteDAO
from api.annotation.data.dao.picture_dao import PictureDAO
from api.annotation.data.model.picture import Picture
from api.annotation.service.note.note_service import NoteService
from api.annotation.service.note.picture.picture_validator import PictureValidator
from ipsum.data.dao.dao import ID
from ipsum.service.detail_crud_service import DetailCRUDService
from ipsum.util.service.collection_tree import CollectionItem, CollectionTree

class PictureService(DetailCRUDService):

    NAME = 'pictures'

    fields_inserted_by_default = [Picture.parent_field]

    def __init__(self) -> None:        
        picture_dao = PictureDAO()
        
        collection_tree = CollectionTree(
            parent=CollectionItem(
                name=NoteService.NAME,
                dao=NoteDAO(),
                parent_field=None,
                id=None,
                field=picture_dao.model.parent_field
            ),
            child=CollectionItem(
                name=self.NAME,
                parent_field=picture_dao.model.parent_field,
                dao=picture_dao,
                id=None,
                field=ID
            )
        )

        super().__init__(
            dao=collection_tree.child.dao,
            validator=PictureValidator(
                dao=collection_tree.child.dao, 
                parent_dao=collection_tree.parent.dao
            ), 
            collection_tree=collection_tree
        )
