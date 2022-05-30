
# TODO Testar CollectionTree

from pytest import raises
from arq.data.dao.dao import Dao

from arq.exception.arq_exception import ArqException
from arq.exception.exception_message import COLLECTION_TREE_ALL_DAO_ATTRIBUTES_MUST_BE_A_DAO, COLLECTION_TREE_ALL_ITEMS_MUST_BE_A_COLLECTION_ITEM, COLLECTION_TREE_MUST_HAVE_AT_LEAST_2_ITEM
from arq.util.service.collection_tree import DAO_ATTRIBUTE, CollectionItem, CollectionTree


class TestCollectionTree:

    class TestModel:
        pass

    def test_have_at_least_2_items(self):

        with raises(ArqException, match=COLLECTION_TREE_MUST_HAVE_AT_LEAST_2_ITEM.format(CollectionTree.__class__)):
            collection_tree = [
                CollectionItem('test', 'test_parent_field', None, Dao(self.TestModel), 'test_field')
            ]

            CollectionTree(collection_tree)

    def test_all_items_must_be_an_instance_of_collection_item(self):
        class ErrorTestClass:
            pass

        class TestClass(CollectionItem):
            pass

        with raises(ArqException, match=COLLECTION_TREE_ALL_ITEMS_MUST_BE_A_COLLECTION_ITEM.format(CollectionItem, CollectionItem, ErrorTestClass)):
            collection_tree = [
                CollectionItem('test 1', 'test_parent_field', None, Dao(self.TestModel), 'test_field'),
                TestClass('test 2', 'test_parent_field', None, Dao(self.TestModel), 'test_field'),
                ErrorTestClass(),
                CollectionItem('test 4', 'test_parent_field', None, Dao(self.TestModel), 'test_field')
            ]

            CollectionTree(collection_tree)

    def test_all_daos_in_collection_items_must_be_an_instance_of_dao(self):
        class NotDAO:
            pass

        class OtherDAO(Dao):
            pass

        class TestCollectionItem(CollectionItem):
            pass

        error_item = TestCollectionItem('test 3', 'test_parent_field', None, NotDAO(), 'test_field')
        collection_tree = [
                CollectionItem('test 1', 'test_parent_field', None, Dao(self.TestModel), 'test_field'),
                CollectionItem('test 2', 'test_parent_field', None, OtherDAO(self.TestModel), 'test_field'),
                error_item,
                CollectionItem('test 4', 'test_parent_field', None, Dao(self.TestModel), 'test_field')
            ]

        with raises(ArqException, match=COLLECTION_TREE_ALL_DAO_ATTRIBUTES_MUST_BE_A_DAO.format(DAO_ATTRIBUTE, CollectionItem, Dao, NotDAO, TestCollectionItem, error_item.name)):
            CollectionTree(collection_tree)



        
        
        