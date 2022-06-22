
from pytest import raises
from ipsum.data.dao.crud_dao import CRUDDAO
from ipsum.data.dao.detail_crud_dao import DetailCRUDDAO
from ipsum.exception.exception_message import DETAIL_CRUD_DAO_MODEL_WITHOUT_PARENT_FIELD
from ipsum.tests.resources.data.model.ipsum_test_model import IpsumTestModel
from ipsum.tests.resources.data.model.detail_test_model import DetailTestModel
from ipsum.util.data.pagination import Pagination
from ipsum.util.enviroment_variable import get_database_url
from ipsum.util.test.database_test import DatabaseTest
from ipsum.exception.ipsum_exception import IpsumException

class TestDetailCRUDDAO:

    TEST_DB_URI = get_database_url()

    FAKE_ID = '6248620366564103f229595f'

    OTHER_FAKE_ID = '627ffd74ee52c2e97a757b86'

    detail_crud_dao = DetailCRUDDAO(model=DetailTestModel)

    model = detail_crud_dao.model

    parent_dao = CRUDDAO(model=IpsumTestModel)

    parent = parent_dao.model

    def test_model_has_attribute_parent_field(self):
        
        def _test_must_raise_exception():
            class TestModel:
                pass 

            class TestDetailCRUDDAO(DetailCRUDDAO):
                pass

            with raises(IpsumException, match=DETAIL_CRUD_DAO_MODEL_WITHOUT_PARENT_FIELD.format(TestModel, DetailCRUDDAO.__class__, TestDetailCRUDDAO, TestDetailCRUDDAO.PARENT_FIELD)):
                TestDetailCRUDDAO(model=TestModel)           
        
        _test_must_raise_exception()

        def _test_must_raise_exception_if_is_none():
            class TestModel:
                parent_field = None
                pass 

            class TestDetailCRUDDAO(DetailCRUDDAO):
                pass

            with raises(IpsumException, match=DETAIL_CRUD_DAO_MODEL_WITHOUT_PARENT_FIELD.format(TestModel, DetailCRUDDAO.__class__, TestDetailCRUDDAO, TestDetailCRUDDAO.PARENT_FIELD)):
                TestDetailCRUDDAO(model=TestModel)           
        
        _test_must_raise_exception_if_is_none()

        def _test_not_must_raise_exception():
            class TestModel:
                parent_field = 'test_parent_field'
                pass 

            class TestDetailCRUDDAO(DetailCRUDDAO):
                pass

            TestDetailCRUDDAO(model=TestModel)           
        
        _test_not_must_raise_exception()

    def test_find_by_parent_id(self):

        database_test = DatabaseTest(host=self.TEST_DB_URI)

        parent_doc = self.parent(
            id=self.FAKE_ID,
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
        
        database_test.add_data(self.detail_crud_dao, [model_doc_1, model_doc_2], parent_ids=[self.FAKE_ID])

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
        database_test.add_data(self.detail_crud_dao, [other_model_doc_1, other_model_doc_2], parent_ids=[self.OTHER_FAKE_ID])

        @database_test.persistence_test()
        def _():

            childs = self.detail_crud_dao.find(parent_doc.id)

            for child in childs:
                child_id = child.id

                assert model_doc_1.id == child_id or model_doc_2.id == child_id

        _()

    def test_paginate_by_parent_id(self):

        database_test = DatabaseTest(host=self.TEST_DB_URI)

        parent_doc = self.parent(
            id=self.FAKE_ID,
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
        
        database_test.add_data(self.detail_crud_dao, [model_doc_1, model_doc_2], parent_ids=[self.FAKE_ID])

        other_parent_doc = self.parent(
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
        database_test.add_data(self.detail_crud_dao, [other_model_doc_1, other_model_doc_2], parent_ids=[self.OTHER_FAKE_ID])

        @database_test.persistence_test()
        def _():

            pagination = self.detail_crud_dao.paginate(parent_doc.id)

            for child in pagination[Pagination.ITEMS]:
                child_id = child.id

                assert model_doc_1.id == child_id or model_doc_2.id == child_id

            pagination_info = pagination[Pagination.INFO]

            assert pagination_info[Pagination.OFFSET] == 0
            assert pagination_info[Pagination.LIMIT] == 5
            assert pagination_info[Pagination.TOTAL] == 2
            assert pagination_info[Pagination.EMPTY] == False

        _()



