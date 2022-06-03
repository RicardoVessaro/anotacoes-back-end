
from pytest import raises
from ipsum.data.dao.crud_dao import CRUDDAO
from ipsum.exception.ipsum_exception import IpsumException
from ipsum.exception.exception_message import OBJECT_NOT_FOUND_EXCEPTION_MESSAGE
from ipsum.tests.resources.data.model.ipsum_test_model import IpsumTestModel
from ipsum.util.enviroment_variable import get_test_database_url
from ipsum.util.test.database_test import DatabaseTest


class TestCRUDDao:

    TEST_DB_URI = get_test_database_url()

    crud_dao = CRUDDAO(model=IpsumTestModel)

    model = crud_dao.model

    def test_insert(self):
        ipsum_test_model = IpsumTestModel(code=1, title='test_insert_TestCRUDDao')

        database_test = DatabaseTest(host=self.TEST_DB_URI, daos_to_clean=[self.crud_dao])
        def _():
            
            @database_test.persistence_test()
            def test_insert_using_model():
                inserted_model = self.crud_dao.insert(ipsum_test_model)
                db_model = self.model.objects().first()

                assert inserted_model.id == db_model.id
            test_insert_using_model()

            @database_test.persistence_test()
            def test_insert_using_dict():
                model_dict = {
                    "code":2, "title":'test_insert_TestCRUDDao'
                }

                inserted_model = self.crud_dao.insert(model_dict)
                db_model = self.model.objects().first()

                assert inserted_model.code == db_model.code
            test_insert_using_dict()

        _()

    def test_delete(self):

        ipsum_test_model, database_test = self._build_default_model_and_ipsum_test(1, 'test_delete_TestCRUDDao')
        
        @database_test.persistence_test()
        def _():
            ipsum_test_model_id = str(ipsum_test_model.id)

            deleted_id = self.crud_dao.delete(ipsum_test_model_id)

            assert deleted_id == ipsum_test_model_id

            assert self.crud_dao.find_by_id(ipsum_test_model_id) is None

            with raises(IpsumException, match=OBJECT_NOT_FOUND_EXCEPTION_MESSAGE.format(deleted_id)):
                self.crud_dao.delete(deleted_id)

        _()

    def test_update(self):

        ipsum_test_model, database_test = self._build_default_model_and_ipsum_test(1, 'test_update_TestCRUDDao', True)

        @database_test.persistence_test()
        def test_update_using_dict():
            model_id = ipsum_test_model.id 

            changes = {
                "title": "test_update_TestCRUDDao Updated",
                "boolean": False,
	            "code": 2,
            }

            updated_model = self.crud_dao.update(model_id, changes)
            database_model = self.crud_dao.find_by_id(model_id)

            assert updated_model.id == database_model.id == model_id
            assert updated_model.title == database_model.title == changes["title"]
            assert updated_model.boolean == database_model.boolean == changes["boolean"]
            assert updated_model.code == database_model.code == changes["code"]

        test_update_using_dict()

        ipsum_test_model, database_test = self._build_default_model_and_ipsum_test(1, 'test_update_TestCRUDDao', True)

        @database_test.persistence_test()
        def test_update_using_model():
            model_id = ipsum_test_model.id 

            changes = ipsum_test_model
            changes.title = "test_update_TestCRUDDao Updated"
            changes.boolean = False 
            changes.code = 2

            updated_model = self.crud_dao.update(model_id, changes)
            database_model = self.crud_dao.find_by_id(model_id)

            assert updated_model.id == database_model.id == model_id
            assert updated_model.title == database_model.title == changes.title
            assert updated_model.boolean == database_model.boolean == changes.boolean
            assert updated_model.code == database_model.code == changes.code

        test_update_using_model()

        def must_raise_exception_when_model_not_exists():
            ipsum_test_model, database_test = self._build_default_model_and_ipsum_test(1, 'test_delete_TestCRUDDao')
        
            @database_test.persistence_test()
            def _():
                ipsum_test_model_id = str(ipsum_test_model.id)

                self.crud_dao.delete(ipsum_test_model_id)

                with raises(IpsumException, match=OBJECT_NOT_FOUND_EXCEPTION_MESSAGE.format(ipsum_test_model_id)):
                    self.crud_dao.update(ipsum_test_model_id, ipsum_test_model)

            _()
        must_raise_exception_when_model_not_exists()

    def _build_default_model_and_ipsum_test(self, code, title, boolean=False):
        ipsum_test_model = IpsumTestModel(code=code, title=title, boolean=boolean)

        database_test = DatabaseTest(host=self.TEST_DB_URI)
        database_test.add_data(self.crud_dao, ipsum_test_model)
        
        return ipsum_test_model, database_test