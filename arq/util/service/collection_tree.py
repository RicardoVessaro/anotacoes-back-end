
from collections import namedtuple
from arq.data.dao.dao import Dao

from arq.exception.arq_exception import ArqException
from arq.exception.exception_message import COLLECTION_TREE_ALL_DAO_ATTRIBUTES_MUST_BE_A_DAO, COLLECTION_TREE_ALL_ITEMS_MUST_BE_A_COLLECTION_ITEM, COLLECTION_TREE_MUST_HAVE_AT_LEAST_2_ITEM

DAO_ATTRIBUTE = "dao"
CollectionItem = namedtuple('CollectionItem', f'name parent_field id {DAO_ATTRIBUTE} field')

class CollectionTree:

    def __init__(self, collection_tree) -> None:
        self._validate_collection(collection_tree)

        self._collection_tree = collection_tree 

    @property
    def child(self):
        return self._collection_tree[-1]

    @property
    def parent(self):
        return self._collection_tree[-2]
    
    def _validate_collection(self, collection_tree):
        self._validate_length(collection_tree)

        for collection_item in collection_tree:
            self._validate_is_collection_item(collection_item)

            self._validate_have_dao(collection_item)

    def _validate_have_dao(self, collection_item):
        if not isinstance(collection_item.dao, Dao):
            raise ArqException(COLLECTION_TREE_ALL_DAO_ATTRIBUTES_MUST_BE_A_DAO.format(DAO_ATTRIBUTE, CollectionItem, Dao, collection_item.dao.__class__, collection_item.__class__, collection_item.name))

    def _validate_is_collection_item(self, collection_item):
        if not isinstance(collection_item, CollectionItem):
            raise ArqException(COLLECTION_TREE_ALL_ITEMS_MUST_BE_A_COLLECTION_ITEM.format(CollectionItem, CollectionItem, collection_item.__class__))

    def _validate_length(self, collection_tree):
        if len(collection_tree) < 2:
            raise ArqException(COLLECTION_TREE_MUST_HAVE_AT_LEAST_2_ITEM.format(CollectionTree.__class__))

    def __len__(self):
        return len(self._collection_tree)

    def __getitem__(self, index):
        return self._collection_tree[index]

    def __repr__(self):
        repr = 'CollectionTree: '

        first = True

        for c in self:
            if first:
                repr += c.name

            else:
                repr += f'/{c.name}'

            first = False

        return repr
