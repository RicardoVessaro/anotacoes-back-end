
from collections import namedtuple

CollectionItem = namedtuple('CollectionItem', 'name parent_field id dao field')

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
        # TODO  Validar
        # validar se possui pelo menos 2 items
        # validar se os itens possuem os atributos name, parent_field, id, dao,
        # validar se dao é instancia de DAO
        pass

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
