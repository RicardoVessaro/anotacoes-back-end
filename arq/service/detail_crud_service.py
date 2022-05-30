
from arq.data.dao.detail_crud_dao import DetailCRUDDAO
from arq.service.crud_service import CRUDService
from arq.service.detail_crud_validator import DetailCRUDValidator
from arq.util.service.collection_tree import CollectionTree

class DetailCRUDService(CRUDService):
    
    def __init__(self, dao:DetailCRUDDAO, validator:DetailCRUDValidator, collection_tree:CollectionTree, non_editable_fields=[]) -> None:
        super().__init__(dao, validator, non_editable_fields)

        self._collection_tree = collection_tree

    @property
    def collection_tree(self):
        return self._collection_tree

    def build_collection_tree_ids(self, ids):
        new_collection_tree = []

        for item in self.collection_tree:
            if item.field in ids:
                new_collection_tree.append(item._replace(id=ids[item.field]))
            
            else:
                new_collection_tree.append(item)

        return CollectionTree(collection_tree=new_collection_tree)


    def validate_collection_tree(self, collection_tree):
        self.validator.validate_collection_tree(collection_tree)

    def find(self, parent_id, **query_filter):
        return self._dao.find(parent_id, **query_filter)

    def paginate(self, parent_id, page=1, limit=5, **query_filter):
        return self._dao.paginate(parent_id, page=page, limit=limit, **query_filter)