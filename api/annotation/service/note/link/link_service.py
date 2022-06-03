
from api.annotation.data.dao.link_dao import LinkDAO
from api.annotation.data.model.link import Link
from api.annotation.service.note.link.link_validator import LinkValidator
from ipsum.service.detail_crud_service import DetailCRUDService
from api.annotation.data.dao.note_dao import NoteDAO
from ipsum.util.service.collection_tree import CollectionItem, CollectionTree
from api.annotation.service.note.note_service import NoteService

class LinkService(DetailCRUDService):

    NAME = 'links'

    fields_inserted_by_default = [Link.parent_field]

    def __init__(self) -> None:
        link_dao = LinkDAO()

        collection_tree = CollectionTree(
            parent=CollectionItem(
                name=NoteService.NAME,
                parent_field=None,
                id=None,
                dao=NoteDAO(),
                field=link_dao.model.parent_field
            ),
            child=CollectionItem(
                name=self.NAME,
                parent_field=link_dao.model.parent_field,
                id=None,
                dao=link_dao,
                field='id'
            )
        )

        super().__init__(
            dao=link_dao, 
            validator=LinkValidator(
                dao=collection_tree.child.dao,
                parent_dao=collection_tree.parent.dao
            ), 
            collection_tree=collection_tree)
