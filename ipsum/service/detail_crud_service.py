
from ipsum.data.dao.detail_crud_dao import DetailCRUDDAO
from ipsum.service.crud_service import CRUDService
from ipsum.service.detail_crud_validator import DetailCRUDValidator
from ipsum.util.service.collection_tree import CollectionTree

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

        return CollectionTree(parent=new_collection_tree[0], child=new_collection_tree[1])


    def validate_collection_tree(self, collection_tree):
        self.validator.validate_collection_tree(collection_tree)

    def find(self, parent_id, **query_filter):
        return self._dao.find(parent_id, **query_filter)

    def paginate(self, parent_id, offset=0, limit=5, **query_filter):
        return self._dao.paginate(parent_id, offset=offset, limit=limit, **query_filter)