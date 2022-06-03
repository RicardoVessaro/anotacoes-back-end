
from collections import namedtuple
from arq.data.dao.dao import DAO

from arq.exception.ipsum_exception import IpsumException
from arq.exception.exception_message import COLLECTION_TREE_ALL_DAO_ATTRIBUTES_MUST_BE_A_DAO, COLLECTION_TREE_ALL_ITEMS_MUST_BE_A_COLLECTION_ITEM, COLLECTION_TREE_ITEMS_WITH_DUPLICATED_NAMES, COLLECTION_TREE_MUST_HAVE_AT_LEAST_2_ITEM

DAO_ATTRIBUTE = "dao"
CollectionItem = namedtuple('CollectionItem', f'name parent_field id {DAO_ATTRIBUTE} field')

class CollectionTree:

    def __init__(self, parent, child) -> None:
        collection_tree = [parent, child] 
        self._validate_collection(collection_tree)

        self._parent = parent
        self._child = child

        self._collection_tree = collection_tree

    @property
    def child(self):
        return self._child

    @property
    def parent(self):
        return self._parent

    def is_parent(self, collection_item):
        return collection_item.name == self.parent.name

    def is_child(self, collection_item):
        return collection_item.name == self.child.name

    def get_url(self):
        url = ''

        first = True

        count = 1
        for c in self:

            if not first:
                url += '/'

            if count == len(self):
                url += f'{c.name}/'

            else:
                url += f'{c.name}/<{c.field}>'

            first = False
            count += 1

        return url

    def _validate_collection(self, collection_tree):

        used_names = []        
        for collection_item in collection_tree:
            self._validate_is_collection_item(collection_item)

            used_names = self._validate_unique_name(collection_item, used_names)

            self._validate_have_dao(collection_item)

    def _validate_unique_name(self, collection_item, used_names):
        name = collection_item.name

        if name in used_names:
            raise IpsumException(COLLECTION_TREE_ITEMS_WITH_DUPLICATED_NAMES.format(name, CollectionItem))
        else:
            used_names.append(name)

        return used_names        

    def _validate_have_dao(self, collection_item):
        if not isinstance(collection_item.dao, DAO):
            raise IpsumException(COLLECTION_TREE_ALL_DAO_ATTRIBUTES_MUST_BE_A_DAO.format(DAO_ATTRIBUTE, CollectionItem, DAO, collection_item.dao.__class__, collection_item.__class__, collection_item.name))

    def _validate_is_collection_item(self, collection_item):
        if not isinstance(collection_item, CollectionItem):
            raise IpsumException(COLLECTION_TREE_ALL_ITEMS_MUST_BE_A_COLLECTION_ITEM.format(CollectionItem, CollectionItem, collection_item.__class__))

    def __len__(self):
        return len(self._collection_tree)

    def __getitem__(self, index):
        return self._collection_tree[index]

    def __repr__(self):
        repr = f'{self.__class__}: '

        first = True

        for c in self:
            if first:
                repr += c.name

            else:
                repr += f'/{c.name}'

            first = False

        return repr
