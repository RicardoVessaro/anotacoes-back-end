
from pytest import raises
from arq.data.dao.dao import DAO

from arq.exception.arq_exception import ArqException
from arq.exception.exception_message import COLLECTION_TREE_ALL_DAO_ATTRIBUTES_MUST_BE_A_DAO, COLLECTION_TREE_ALL_ITEMS_MUST_BE_A_COLLECTION_ITEM, COLLECTION_TREE_ITEMS_WITH_DUPLICATED_NAMES, COLLECTION_TREE_MUST_HAVE_AT_LEAST_2_ITEM
from arq.util.service.collection_tree import DAO_ATTRIBUTE, CollectionItem, CollectionTree


class TestCollectionTree:

    class TestModel:
        pass

    def test_have_at_least_2_items(self):

        with raises(ArqException, match=COLLECTION_TREE_MUST_HAVE_AT_LEAST_2_ITEM.format(CollectionTree.__class__)):
            collection_tree = [
                CollectionItem('test', 'test_parent_field', None, DAO(self.TestModel), 'test_field')
            ]

            CollectionTree(collection_tree)

    def test_all_items_must_be_an_instance_of_collection_item(self):
        class ErrorTestClass:
            pass

        class TestClass(CollectionItem):
            pass

        with raises(ArqException, match=COLLECTION_TREE_ALL_ITEMS_MUST_BE_A_COLLECTION_ITEM.format(CollectionItem, CollectionItem, ErrorTestClass)):
            collection_tree = [
                CollectionItem('test 1', 'test_parent_field', None, DAO(self.TestModel), 'test_field'),
                TestClass('test 2', 'test_parent_field', None, DAO(self.TestModel), 'test_field'),
                ErrorTestClass(),
                CollectionItem('test 4', 'test_parent_field', None, DAO(self.TestModel), 'test_field')
            ]

            CollectionTree(collection_tree)

    def test_all_daos_in_collection_items_must_be_an_instance_of_dao(self):
        class NotDAO:
            pass

        class OtherDAO(DAO):
            pass

        class TestCollectionItem(CollectionItem):
            pass

        error_item = TestCollectionItem('test 3', 'test_parent_field', None, NotDAO(), 'test_field')
        collection_tree = [
                CollectionItem('test 1', 'test_parent_field', None, DAO(self.TestModel), 'test_field'),
                CollectionItem('test 2', 'test_parent_field', None, OtherDAO(self.TestModel), 'test_field'),
                error_item,
                CollectionItem('test 4', 'test_parent_field', None, DAO(self.TestModel), 'test_field')
            ]

        with raises(ArqException, match=COLLECTION_TREE_ALL_DAO_ATTRIBUTES_MUST_BE_A_DAO.format(DAO_ATTRIBUTE, CollectionItem, DAO, NotDAO, TestCollectionItem, error_item.name)):
            CollectionTree(collection_tree)

    def test_must_raise_exception_when_collection_item_have_duplicated_name(self):
        name = 'duplicated test'
        collection_items = [
            CollectionItem(name, None, None, DAO(self.TestModel), 'test_field_1'),
            CollectionItem('test', 'test_parent_field', None, DAO(self.TestModel), 'test_field_2'),
            CollectionItem('other test', 'test_parent_field', None, DAO(self.TestModel), 'test_field_3'),
            CollectionItem(name, 'test_parent_field', None, DAO(self.TestModel), 'test_field_4'),
        ]

        with raises(ArqException, match=COLLECTION_TREE_ITEMS_WITH_DUPLICATED_NAMES.format(name, CollectionItem)):
            CollectionTree(collection_items)

    def test_child(self):
        child = CollectionItem('test 3', 'test_parent_field', None, DAO(self.TestModel), 'test_field_3')

        collection_items = [
            CollectionItem('test 1', None, None, DAO(self.TestModel), 'test_field_1'),
            CollectionItem('test 2', 'test_parent_field', None, DAO(self.TestModel), 'test_field_2'),
            child,
        ]

        collection_tree = CollectionTree(collection_items)

        assert collection_tree.child == child

    def test_parent(self):
        parent = CollectionItem('test 2', 'test_parent_field', None, DAO(self.TestModel), 'test_field_2')

        collection_items = [
            CollectionItem('test 1', None, None, DAO(self.TestModel), 'test_field_1'),
            parent,
            CollectionItem('test 3', 'test_parent_field', None, DAO(self.TestModel), 'test_field_3')
        ]

        collection_tree = CollectionTree(collection_items)

        assert collection_tree.parent == parent

    def test_is_parent(self):
        parent = CollectionItem('test 2', 'test_parent_field', None, DAO(self.TestModel), 'test_field_2')

        collection_items = [
            CollectionItem('test 1', None, None, DAO(self.TestModel), 'test_field_1'),
            parent,
            CollectionItem('test 3', 'test_parent_field', None, DAO(self.TestModel), 'test_field_3')
        ]

        collection_tree = CollectionTree(collection_items)

        assert collection_tree.is_parent(parent)
        assert not collection_tree.is_parent(collection_items[0])
        assert not collection_tree.is_parent(collection_items[2])


    def test_is_child(self):
        child = CollectionItem('test 3', 'test_parent_field', None, DAO(self.TestModel), 'test_field_3')

        collection_items = [
            CollectionItem('test 1', None, None, DAO(self.TestModel), 'test_field_1'),
            CollectionItem('test 2', 'test_parent_field', None, DAO(self.TestModel), 'test_field_2'),
            child,
        ]

        collection_tree = CollectionTree(collection_items)

        assert collection_tree.is_child(child)
        assert not collection_tree.is_child(collection_items[0])
        assert not collection_tree.is_child(collection_items[1])


        
        
        