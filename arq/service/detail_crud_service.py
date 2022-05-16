
from arq.service.crud_service import CRUDService
from arq.service.detail_crud_validator import DetailCRUDValidator
from arq.util.service.collection_tree import CollectionTree

class DetailCRUDService(CRUDService):
    
    def __init__(self, dao, validator:DetailCRUDValidator, collection_tree:CollectionTree, non_editable_fields=[]) -> None:
        super().__init__(dao, validator, non_editable_fields)

        self._collection_tree = collection_tree

    @property
    def collection_tree(self):
        return self._collection_tree

    def validate_collection_tree(self):
        self._validator.validate_collection_tree(self.collection_tree)

    def find_by_parent_id(self, parent_id, **query_filter):
        return self._dao.find_by_parent_id(parent_id, **query_filter)

    def paginate_by_parent_id(self, parent_id, page=1, limit=5, **query_filter):
        return self._dao.paginate_by_parent_id(parent_id, page=page, limit=limit, **query_filter)