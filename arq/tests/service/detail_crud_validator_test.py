
from pytest import raises
from arq.data.dao.crud_dao import CRUDDAO
from arq.data.dao.detail_crud_dao import DetailCRUDDAO
from arq.exception.exception_message import CHILD_NOT_FOUND_IN_PARENT, PARENT_OBJECT_NOT_FOUND_EXCEPTION_MESSAGE
from arq.tests.resources.data.model.ipsum_test_model import IpsumTestModel
from arq.tests.resources.data.model.detail_child_test_model import DetailChildTestModel
from arq.tests.resources.data.model.detail_test_model import DetailTestModel
from arq.service.detail_crud_validator import DetailCRUDValidator
from arq.util.enviroment_variable import get_test_database_url
from arq.util.service.collection_tree import CollectionItem, CollectionTree
from arq.util.test.database_test import DatabaseTest
from arq.exception.ipsum_exception import IpsumException

class TestDetailCRUDValidator:

    FAKE_PARENT_ID = '6248620366564103f229595f'

    FAKE_DETAIL_ID = '627ffd74ee52c2e97a757b86'

    TEST_DB_URI = get_test_database_url()

    parent_dao = CRUDDAO(model=IpsumTestModel)
    parent = parent_dao.model

    dao = DetailCRUDDAO(model=DetailTestModel)
    model = dao.model
    detail_crud_validator = DetailCRUDValidator(dao=dao, parent_dao=parent_dao)

    detail_child_dao = DetailCRUDDAO(model=DetailChildTestModel)
    detail_child_model = detail_child_dao.model


    def test_must_raise_exception_when_parent_not_exists(self):
        database_test = DatabaseTest(host=self.TEST_DB_URI)
        @database_test.persistence_test()
        def validate_on_insert():
            
            parent_field = self.dao.model.parent_field
            with raises(IpsumException, match=PARENT_OBJECT_NOT_FOUND_EXCEPTION_MESSAGE.format(parent_field, self.FAKE_PARENT_ID)):

                doc = {'code':1, 'title': 'Detail', 'arq_model_id': self.FAKE_PARENT_ID}
                self.detail_crud_validator.validate_insert(doc)

        validate_on_insert()

        doc = self.model(code=1, title='Detail', arq_model_id=self.FAKE_PARENT_ID)
        database_test = DatabaseTest(host=self.TEST_DB_URI)
        database_test.add_data(self.dao, doc, parent_ids=[self.FAKE_PARENT_ID])
        @database_test.persistence_test()
        def validate_on_update():
            
            parent_field = self.dao.model.parent_field
            with raises(IpsumException, match=PARENT_OBJECT_NOT_FOUND_EXCEPTION_MESSAGE.format(parent_field, self.FAKE_PARENT_ID)):
                
                self.detail_crud_validator.validate_update(doc.id, doc)

        validate_on_update()

    def test_not_must_raise_exception_when_parent_not_exists(self):
        parent_doc = self.parent(code=1, title='Parent')

        database_test = DatabaseTest(host=self.TEST_DB_URI)
        database_test.add_data(self.parent_dao, parent_doc)

        @database_test.persistence_test()
        def validate_on_insert():
            
            doc = {'code':1, 'title': 'Detail', 'arq_model_id': str(parent_doc.id)}
            self.detail_crud_validator.validate_insert(doc)

        validate_on_insert()


        doc = self.model(code=1, title='Detail', arq_model_id=self.FAKE_PARENT_ID)
        parent_doc = self.parent(code=1, title='Parent')

        database_test = DatabaseTest(host=self.TEST_DB_URI)
        database_test.add_data(self.parent_dao, parent_doc)
        database_test.add_data(self.dao, doc, parent_ids=[self.FAKE_PARENT_ID])
        @database_test.persistence_test()
        def validate_on_update():
            doc.arq_model_id = str(parent_doc.id)

            self.detail_crud_validator.validate_update(doc.id, doc)

        validate_on_update()

    def test_validate_collection_tree_must_raise_exception_when_child_not_in_parent(self):
        doc = self.model(code=1, title='Detail', arq_model_id='624786f6590c79c2fb3af557')
        parent_doc = self.parent(code=1, title='Parent', id=self.FAKE_PARENT_ID)

        database_test = DatabaseTest(host=self.TEST_DB_URI)
        database_test.add_data(self.parent_dao, parent_doc)
        database_test.add_data(self.dao, doc, parent_ids=[self.FAKE_PARENT_ID])
        @database_test.persistence_test()
        def _():
            
            arq_model_item = CollectionItem(name='arq_model', parent_field=None, id=parent_doc.id, dao=self.parent_dao, field=self.model.parent_field)
            detail_model_item = CollectionItem(name='detail_model', parent_field=self.model.parent_field, id=str(doc.id), dao=self.dao, field=self.detail_child_model.parent_field)

            collection_tree = CollectionTree(parent=arq_model_item, child=detail_model_item)

            error_msg = CHILD_NOT_FOUND_IN_PARENT.format(
                collection_tree.child.name, collection_tree.child.id, 
                collection_tree.child.parent_field, str(doc.arq_model_id),
                collection_tree.parent.name, collection_tree.parent.id
            )

            with raises(IpsumException, match=error_msg):
                self.detail_crud_validator.validate_collection_tree(collection_tree)

        _()

    def test_validate_collection_tree_must_not_raise_exception(self):
        doc = self.model(code=1, title='Detail', arq_model_id=self.FAKE_PARENT_ID, id=self.FAKE_DETAIL_ID)
        parent_doc = self.parent(code=1, title='Parent', id=self.FAKE_PARENT_ID)
        
        detail_child_doc = self.detail_child_model(code=1, title='Detail', detail_parent_id=self.FAKE_DETAIL_ID)

        database_test = DatabaseTest(host=self.TEST_DB_URI)
        database_test.add_data(self.parent_dao, parent_doc)
        database_test.add_data(self.dao, doc, parent_ids=[self.FAKE_PARENT_ID])
        database_test.add_data(self.detail_child_dao, detail_child_doc, parent_ids=[self.FAKE_DETAIL_ID])
        @database_test.persistence_test()
        def _():
            arq_model_item = CollectionItem(name='arq_model', parent_field=None, id=parent_doc.id, dao=self.parent_dao, field=self.model.parent_field)
            detail_model_item = CollectionItem(name='detail_model', parent_field=self.model.parent_field, id=str(doc.id), dao=self.dao, field=self.detail_child_model.parent_field)

            collection_tree = CollectionTree(parent=arq_model_item, child=detail_model_item)
        
            self.detail_crud_validator.validate_collection_tree(collection_tree)
        _()

    def test_validate_collection_tree_must_not_raise_exception_when_child_id_not_exists(self):
        doc = self.model(code=1, title='Detail', arq_model_id=self.FAKE_PARENT_ID, id=self.FAKE_DETAIL_ID)
        parent_doc = self.parent(code=1, title='Parent', id=self.FAKE_PARENT_ID)
        
        database_test = DatabaseTest(host=self.TEST_DB_URI)
        database_test.add_data(self.parent_dao, parent_doc)
        database_test.add_data(self.dao, doc, parent_ids=[self.FAKE_PARENT_ID])
        @database_test.persistence_test()
        def _():
            arq_model_item = CollectionItem(name='arq_model', parent_field=None, id=parent_doc.id, dao=self.parent_dao, field=self.model.parent_field)
            detail_model_item = CollectionItem(name='detail_child_model', parent_field=self.detail_child_model.parent_field, id=None, dao=self.detail_child_dao, field='id')

            collection_tree = CollectionTree(parent=arq_model_item, child=detail_model_item)
        
            self.detail_crud_validator.validate_collection_tree(collection_tree)
        _()

