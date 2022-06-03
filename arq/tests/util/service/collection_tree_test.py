
from pytest import raises
from arq.data.dao.dao import DAO

from arq.exception.ipsum_exception import IpsumException
from arq.exception.exception_message import COLLECTION_TREE_ALL_DAO_ATTRIBUTES_MUST_BE_A_DAO, COLLECTION_TREE_ALL_ITEMS_MUST_BE_A_COLLECTION_ITEM, COLLECTION_TREE_ITEMS_WITH_DUPLICATED_NAMES, COLLECTION_TREE_MUST_HAVE_AT_LEAST_2_ITEM
from arq.util.service.collection_tree import DAO_ATTRIBUTE, CollectionItem, CollectionTree


class TestCollectionTree:

    class TestModel:
        pass


    def test_all_items_must_be_an_instance_of_collection_item(self):
        class ErrorTestClass:
            pass

        class TestClass(CollectionItem):
            pass

        with raises(IpsumException, match=COLLECTION_TREE_ALL_ITEMS_MUST_BE_A_COLLECTION_ITEM.format(CollectionItem, CollectionItem, ErrorTestClass)):

            CollectionTree(parent=TestClass('test 2', 'test_parent_field', None, DAO(self.TestModel), 'test_field'), child=ErrorTestClass())

    def test_all_daos_in_collection_items_must_be_an_instance_of_dao(self):
        class NotDAO:
            pass

        class OtherDAO(DAO):
            pass

        class TestCollectionItem(CollectionItem):
            pass

        error_item = TestCollectionItem('test 3', 'test_parent_field', None, NotDAO(), 'test_field')

        with raises(IpsumException, match=COLLECTION_TREE_ALL_DAO_ATTRIBUTES_MUST_BE_A_DAO.format(DAO_ATTRIBUTE, CollectionItem, DAO, NotDAO, TestCollectionItem, error_item.name)):
            CollectionTree(parent=CollectionItem('test 1', 'test_parent_field', None, DAO(self.TestModel), 'test_field'), child=error_item)

    def test_must_raise_exception_when_collection_item_have_duplicated_name(self):
        name = 'duplicated test'

        with raises(IpsumException, match=COLLECTION_TREE_ITEMS_WITH_DUPLICATED_NAMES.format(name, CollectionItem)):
            CollectionTree(parent=CollectionItem(name, None, None, DAO(self.TestModel), 'test_field_1'), child=CollectionItem(name, 'test_parent_field', None, DAO(self.TestModel), 'test_field_4'))

    def test_child(self):
        child = CollectionItem('test 3', 'test_parent_field', None, DAO(self.TestModel), 'test_field_3')

        collection_tree = CollectionTree(parent=CollectionItem('test 1', None, None, DAO(self.TestModel), 'test_field_1'), child=child)

        assert collection_tree.child == child

    def test_parent(self):
        parent = CollectionItem('test 2', 'test_parent_field', None, DAO(self.TestModel), 'test_field_2')

        collection_tree = CollectionTree(parent=parent, child=CollectionItem('test 3', 'test_parent_field', None, DAO(self.TestModel), 'test_field_3'))

        assert collection_tree.parent == parent

    def test_is_parent(self):
        parent = CollectionItem('test 1', None, None, DAO(self.TestModel), 'test_field_1')
        child = CollectionItem('test 2', 'test_parent_field', None, DAO(self.TestModel), 'test_field_2')

        collection_tree = CollectionTree(parent=parent, child=child)

        assert collection_tree.is_parent(parent)
        assert not collection_tree.is_parent(child)


    def test_is_child(self):
        parent = CollectionItem('test 1', None, None, DAO(self.TestModel), 'test_field_1')
        child = CollectionItem('test 2', 'test_parent_field', None, DAO(self.TestModel), 'test_field_2')

        collection_tree = CollectionTree(parent=parent, child=child)

        assert collection_tree.is_child(child)
        assert not collection_tree.is_child(parent)
 
    def test_repr(self):
        parent = CollectionItem('parent', None, None, DAO(self.TestModel), 'parent_field_id')
        child = CollectionItem('child', 'parent_field', None, DAO(self.TestModel), 'child_field_id')

        collection_tree = CollectionTree(parent=parent, child=child)
        expect = f'{CollectionTree}: parent/child'

        assert expect == str(collection_tree)
    
    def test_get_url(self):

        parent = CollectionItem('parent', None, None, DAO(self.TestModel), 'parent_field_id')
        child = CollectionItem('child', 'parent_field', None, DAO(self.TestModel), 'child_field_id')

        collection_tree = CollectionTree(parent=parent, child=child)
        expect = 'parent/<parent_field_id>/child/'

        assert expect == collection_tree.get_url()
    

        