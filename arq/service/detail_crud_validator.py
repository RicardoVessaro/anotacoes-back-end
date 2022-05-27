
from arq.exception.arq_exception import ArqException
from arq.exception.exception_message import CHILD_NOT_FOUND_IN_PARENT, PARENT_OBJECT_NOT_FOUND_EXCEPTION_MESSAGE
from arq.service.crud_validator import CRUDValidator
from arq.util.service.collection_tree import CollectionTree


class DetailCRUDValidator(CRUDValidator):

    def __init__(self, dao, parent_dao, required_fields=[]) -> None:
        super().__init__(dao, required_fields)

        self._parent_dao = parent_dao
        self._parent_field = self._dao.model.parent_field
        self.required_fields.extend([self._parent_field])

    def validate_insert(self, body):
        self._validate_parent_exists(body)

        super().validate_insert(body)

    def validate_update(self, id, body):
        self._validate_parent_exists(body)

        return super().validate_update(id, body)

    def validate_collection_tree(self, collection_tree: CollectionTree):
        for i in range(len(collection_tree) - 1 ):

            child_collection_item = collection_tree[i + 1]

            child_id = child_collection_item.id

            if not child_id is None:
                child = child_collection_item.dao.find_by_id(child_id)

                if not child is None:
                    parent_collection_item = collection_tree[i]

                    parent_id_in_child_doc = str(child[child_collection_item.parent_field])

                    if not parent_id_in_child_doc == str(parent_collection_item.id):
                        parent_id = parent_collection_item.id
                        
                        raise ArqException(CHILD_NOT_FOUND_IN_PARENT.format(
                            child_collection_item.name,
                            child_id,
                            child_collection_item.parent_field,
                            parent_id_in_child_doc,
                            parent_collection_item.name,
                            parent_id
                        ))

    def _validate_parent_exists(self, body):

        parent_id = body[self._parent_field]

        parent = self._parent_dao.find_by_id(parent_id)

        if parent is None:
            raise ArqException(PARENT_OBJECT_NOT_FOUND_EXCEPTION_MESSAGE.format(self._parent_field, parent_id))


