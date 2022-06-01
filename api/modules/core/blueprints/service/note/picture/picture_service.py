
from api.modules.core.blueprints.data.dao.note_dao import NoteDAO
from api.modules.core.blueprints.data.dao.picture_dao import PictureDAO
from api.modules.core.blueprints.data.model.picture import Picture
from api.modules.core.blueprints.service.note.note_service import NoteService
from api.modules.core.blueprints.service.note.picture.picture_validator import PictureValidator
from arq.service.detail_crud_service import DetailCRUDService
from arq.util.service.collection_tree import CollectionItem, CollectionTree

class PictureService(DetailCRUDService):

    NAME = 'picture'

    fields_inserted_by_default = [Picture.parent_field]

    def __init__(self) -> None:        
        picture_dao = PictureDAO()
        
        collection_tree = CollectionTree(collection_tree=[
            CollectionItem(
                name=NoteService.NAME,
                dao=NoteDAO(),
                parent_field=None,
                id=None,
                field=picture_dao.model.parent_field
            ),
            CollectionItem(
                name=self.NAME,
                parent_field=picture_dao.model.parent_field,
                dao=picture_dao,
                id=None,
                field='id'
            )
        ])

        super().__init__(
            dao=collection_tree.child.dao,
            validator=PictureValidator(
                dao=collection_tree.child.dao, 
                parent_dao=collection_tree.parent.dao
            ), 
            collection_tree=collection_tree
        )
