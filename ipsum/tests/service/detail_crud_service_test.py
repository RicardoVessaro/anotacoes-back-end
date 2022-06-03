

from pytest import raises
from ipsum.data.dao.crud_dao import CRUDDAO
from ipsum.data.dao.detail_crud_dao import DetailCRUDDAO
from ipsum.exception.ipsum_exception import IpsumException
from ipsum.exception.exception_message import CHILD_NOT_FOUND_IN_PARENT
from ipsum.service.detail_crud_service import DetailCRUDService
from ipsum.service.detail_crud_validator import DetailCRUDValidator
from ipsum.tests.resources.data.model.ipsum_test_model import IpsumTestModel
from ipsum.tests.resources.data.model.detail_child_test_model import DetailChildTestModel
from ipsum.tests.resources.data.model.detail_test_model import DetailTestModel
from ipsum.util.enviroment_variable import get_test_database_url
from ipsum.util.service.collection_tree import CollectionItem, CollectionTree
from ipsum.util.test.database_test import DatabaseTest


class TestDetailCRUDService:

    FAKE_PARENT_ID = '6248620366564103f229595f'

    FAKE_DETAIL_ID = '627ffd74ee52c2e97a757b86'

    OTHER_FAKE_ID = '624786f6590c79c2fb3af557'

    TEST_DB_URI = get_test_database_url()

    parent_dao = CRUDDAO(model=IpsumTestModel)
    parent = parent_dao.model

    dao = DetailCRUDDAO(model=DetailTestModel)
    model = dao.model
    detail_crud_validator = DetailCRUDValidator(dao=dao, parent_dao=parent_dao)
    detail_crud_service = DetailCRUDService(dao=dao, validator=detail_crud_validator, collection_tree=None)

    detail_child_dao = DetailCRUDDAO(model=DetailChildTestModel)
    detail_child_model = detail_child_dao.model

    def test_find_by_parent_id(self):

        database_test = DatabaseTest(host=self.TEST_DB_URI)

        parent_doc = self.parent(
            id=self.FAKE_PARENT_ID,
            code=1,
            title='Parent'
        )
        database_test.add_data(self.parent_dao, parent_doc)

        model_doc_1 = self.model(
            code=11,
            title='Model',
            ipsum_model_id=parent_doc.id
        )

        model_doc_2 = self.model(
            code=12,
            title='Model',
            ipsum_model_id=parent_doc.id
        )
        
        database_test.add_data(self.dao, [model_doc_1, model_doc_2], parent_ids=[parent_doc.id])

        other_parent_doc = self.parent(
            id=self.OTHER_FAKE_ID,
            code=1,
            title='Parent'
        )
        database_test.add_data(self.parent_dao, other_parent_doc)

        other_model_doc_1 = self.model(
            code=11,
            title='Model',
            ipsum_model_id=self.OTHER_FAKE_ID
        )

        other_model_doc_2 = self.model(
            code=12,
            title='Model',
            ipsum_model_id=self.OTHER_FAKE_ID
        )
        database_test.add_data(self.dao, [other_model_doc_1, other_model_doc_2], parent_ids=[self.OTHER_FAKE_ID])

        @database_test.persistence_test()
        def _():

            childs = self.detail_crud_service.find(parent_doc.id)

            for child in childs:
                child_id = child.id

                assert model_doc_1.id == child_id or model_doc_2.id == child_id

        _()

    def test_paginate_by_parent_id(self):

        database_test = DatabaseTest(host=self.TEST_DB_URI)

        parent_doc = self.parent(
            id=self.FAKE_PARENT_ID,
            code=1,
            title='Parent'
        )
        database_test.add_data(self.parent_dao, parent_doc)

        model_doc_1 = self.model(
            code=11,
            title='Model',
            ipsum_model_id=parent_doc.id
        )

        model_doc_2 = self.model(
            code=12,
            title='Model',
            ipsum_model_id=parent_doc.id
        )
        
        database_test.add_data(self.dao, [model_doc_1, model_doc_2], parent_ids=[parent_doc.id])

        other_parent_doc = self.parent(
            id=self.OTHER_FAKE_ID,
            code=1,
            title='Parent'
        )
        database_test.add_data(self.parent_dao, other_parent_doc)

        other_model_doc_1 = self.model(
            code=11,
            title='Model',
            ipsum_model_id=self.OTHER_FAKE_ID
        )

        other_model_doc_2 = self.model(
            code=12,
            title='Model',
            ipsum_model_id=self.OTHER_FAKE_ID
        )
        database_test.add_data(self.dao, [other_model_doc_1, other_model_doc_2], parent_ids=[self.OTHER_FAKE_ID])

        @database_test.persistence_test()
        def _():

            pagination = self.detail_crud_service.paginate(parent_doc.id)

            for child in pagination['items']:
                child_id = child.id

                assert model_doc_1.id == child_id or model_doc_2.id == child_id

            assert pagination['page'] == 1
            assert pagination['limit'] == 5
            assert pagination['total'] == 2
            assert pagination['has_prev'] == False
            assert pagination['has_next'] == False

        _()

    def test_validate_collection_tree_must_raise_exception_when_child_not_in_parent(self):
        doc = self.model(code=1, title='Detail', ipsum_model_id=self.FAKE_PARENT_ID)
        parent_doc = self.parent(code=1, title='Parent', id=self.FAKE_PARENT_ID)
        detail_child_doc = self.detail_child_model(code=1, title='Detail', detail_parent_id=self.FAKE_DETAIL_ID)

        database_test = DatabaseTest(host=self.TEST_DB_URI)
        database_test.add_data(self.parent_dao, parent_doc)
        database_test.add_data(self.dao, doc, parent_ids=[doc.ipsum_model_id])
        database_test.add_data(self.detail_child_dao, detail_child_doc, parent_ids=[detail_child_doc.detail_parent_id])
        @database_test.persistence_test()
        def _():
            
            ipsum_model_item = CollectionItem(name='ipsum_model', parent_field=None, id=parent_doc.id, dao=self.parent_dao, field=self.model.parent_field)
            detail_model_item = CollectionItem(name='detail_child_model', parent_field=self.detail_child_model.parent_field, id=str(detail_child_doc.id), dao=self.detail_child_dao, field='id')

            collection_tree = CollectionTree(parent=ipsum_model_item, child=detail_model_item)

            _detail_crud_service = DetailCRUDService(dao=self.dao, validator=self.detail_crud_validator, collection_tree=collection_tree)

            error_msg = CHILD_NOT_FOUND_IN_PARENT.format(
                collection_tree.child.name, collection_tree.child.id, 
                collection_tree.child.parent_field, str(detail_child_doc.detail_parent_id),
                collection_tree.parent.name, collection_tree.parent.id
            )

            with raises(IpsumException, match=error_msg):
                _detail_crud_service.validate_collection_tree(collection_tree)

        _()

    def test_validate_collection_tree_must_not_raise_exception(self):
        doc = self.model(code=1, title='Detail', ipsum_model_id=self.FAKE_PARENT_ID, id=self.FAKE_DETAIL_ID)
        parent_doc = self.parent(code=1, title='Parent', id=self.FAKE_PARENT_ID)
        
        detail_child_doc = self.detail_child_model(code=1, title='Detail', detail_parent_id=self.FAKE_DETAIL_ID)

        database_test = DatabaseTest(host=self.TEST_DB_URI)
        database_test.add_data(self.parent_dao, parent_doc)
        database_test.add_data(self.dao, doc, parent_ids=[doc.ipsum_model_id])
        database_test.add_data(self.detail_child_dao, detail_child_doc, parent_ids=[detail_child_doc.detail_parent_id])
        @database_test.persistence_test()
        def _():
            ipsum_model_item = CollectionItem(name='ipsum_model', parent_field=None, id=parent_doc.id, dao=self.parent_dao, field=self.model.parent_field)
            detail_model_item = CollectionItem(name='detail_model', parent_field=self.model.parent_field, id=str(doc.id), dao=self.dao, field=self.detail_child_model.parent_field)

            collection_tree = CollectionTree(parent=ipsum_model_item, child=detail_model_item)
        
            _detail_crud_service = DetailCRUDService(dao=self.dao, validator=self.detail_crud_validator, collection_tree=collection_tree)

            _detail_crud_service.validate_collection_tree(collection_tree)
        _()

    def test_validate_collection_tree_must_not_raise_exception_when_child_id_not_exists(self):
        doc = self.model(code=1, title='Detail', ipsum_model_id=self.FAKE_PARENT_ID, id=self.FAKE_DETAIL_ID)
        parent_doc = self.parent(code=1, title='Parent', id=self.FAKE_PARENT_ID)
        
        database_test = DatabaseTest(host=self.TEST_DB_URI)
        database_test.add_data(self.parent_dao, parent_doc)
        database_test.add_data(self.dao, doc, parent_ids=[doc.ipsum_model_id])
        @database_test.persistence_test()
        def _():
            ipsum_model_item = CollectionItem(name='ipsum_model', parent_field=None, id=parent_doc.id, dao=self.parent_dao, field=self.model.parent_field)
            detail_model_item = CollectionItem(name='detail_model', parent_field=self.model.parent_field, id=str(doc.id), dao=self.dao, field=self.detail_child_model.parent_field)

            collection_tree = CollectionTree(parent=ipsum_model_item, child=detail_model_item)
        
            _detail_crud_service = DetailCRUDService(dao=self.dao, validator=self.detail_crud_validator, collection_tree=collection_tree)

            _detail_crud_service.validate_collection_tree(collection_tree)
        _()