
from pytest import raises
from arq.data.dao.crud_dao import CRUDDAO
from arq.exception.arq_exception import ArqException
from arq.exception.exception_message import OBJECT_NOT_FOUND_EXCEPTION_MESSAGE
from arq.tests.resources.data.model.arq_test_model import ArqTestModel
from arq.util.enviroment_variable import get_test_database_url
from arq.util.test.database_test import DatabaseTest


class TestCRUDDao:

    TEST_DB_URI = get_test_database_url()

    arq_crud_dao = CRUDDAO(model=ArqTestModel)

    model = arq_crud_dao._model

    def test_insert(self):
        arq_test_model = ArqTestModel(code=1, title='test_insert_TestArqCRUDDao')

        arq_database_test = DatabaseTest(daos_to_clean=[self.arq_crud_dao])
        def _():
            
            @arq_database_test.persistence_test(host=self.TEST_DB_URI)
            def test_insert_using_model():
                inserted_model = self.arq_crud_dao.insert(arq_test_model)
                db_model = self.model.objects().first()

                assert inserted_model.id == db_model.id
            test_insert_using_model()

            @arq_database_test.persistence_test(host=self.TEST_DB_URI)
            def test_insert_using_dict():
                model_dict = {
                    "code":2, "title":'test_insert_TestArqCRUDDao'
                }

                inserted_model = self.arq_crud_dao.insert(model_dict)
                db_model = self.model.objects().first()

                assert inserted_model.code == db_model.code
            test_insert_using_dict()

        _()

    def test_delete(self):

        arq_test_model, arq_database_test = self._build_default_model_and_arq_test(1, 'test_delete_TestArqCRUDDao')
        
        @arq_database_test.persistence_test(host=self.TEST_DB_URI)
        def _():
            arq_test_model_id = str(arq_test_model.id)

            deleted_id = self.arq_crud_dao.delete(arq_test_model_id)

            assert deleted_id == arq_test_model_id

            assert self.arq_crud_dao.find_by_id(arq_test_model_id) is None

            with raises(ArqException, match=OBJECT_NOT_FOUND_EXCEPTION_MESSAGE.format(deleted_id)):
                self.arq_crud_dao.delete(deleted_id)

        _()

    def test_update(self):

        arq_test_model, arq_database_test = self._build_default_model_and_arq_test(1, 'test_update_TestArqCRUDDao', True)

        @arq_database_test.persistence_test(host=self.TEST_DB_URI)
        def test_update_using_dict():
            model_id = arq_test_model.id 

            changes = {
                "title": "test_update_TestArqCRUDDao Updated",
                "boolean": False,
	            "code": 2,
            }

            updated_model = self.arq_crud_dao.update(model_id, changes)
            database_model = self.arq_crud_dao.find_by_id(model_id)

            assert updated_model.id == database_model.id == model_id
            assert updated_model.title == database_model.title == changes["title"]
            assert updated_model.boolean == database_model.boolean == changes["boolean"]
            assert updated_model.code == database_model.code == changes["code"]

        test_update_using_dict()

        arq_test_model, arq_database_test = self._build_default_model_and_arq_test(1, 'test_update_TestArqCRUDDao', True)

        @arq_database_test.persistence_test(host=self.TEST_DB_URI)
        def test_update_using_model():
            model_id = arq_test_model.id 

            changes = arq_test_model
            changes.title = "test_update_TestArqCRUDDao Updated"
            changes.boolean = False 
            changes.code = 2

            updated_model = self.arq_crud_dao.update(model_id, changes)
            database_model = self.arq_crud_dao.find_by_id(model_id)

            assert updated_model.id == database_model.id == model_id
            assert updated_model.title == database_model.title == changes.title
            assert updated_model.boolean == database_model.boolean == changes.boolean
            assert updated_model.code == database_model.code == changes.code

        test_update_using_model()

        def must_raise_exception_when_model_not_exists():
            arq_test_model, arq_database_test = self._build_default_model_and_arq_test(1, 'test_delete_TestArqCRUDDao')
        
            @arq_database_test.persistence_test(host=self.TEST_DB_URI)
            def _():
                arq_test_model_id = str(arq_test_model.id)

                self.arq_crud_dao.delete(arq_test_model_id)

                with raises(ArqException, match=OBJECT_NOT_FOUND_EXCEPTION_MESSAGE.format(arq_test_model_id)):
                    self.arq_crud_dao.update(arq_test_model_id, arq_test_model)

            _()
        must_raise_exception_when_model_not_exists()

    def _build_default_model_and_arq_test(self, code, title, boolean=False):
        arq_test_model = ArqTestModel(code=code, title=title, boolean=boolean)

        arq_database_test = DatabaseTest()
        arq_database_test.add_data(self.arq_crud_dao, arq_test_model)
        
        return arq_test_model, arq_database_test