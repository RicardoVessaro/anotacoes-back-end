
from pytest import raises
from ipsum.data.dao.crud_dao import CRUDDAO
from ipsum.exception.ipsum_exception import IpsumException
from ipsum.exception.exception_message import OBJECT_NOT_FOUND_EXCEPTION_MESSAGE
from ipsum.service.crud_service import CRUDService
from ipsum.service.crud_validator import CRUDValidator
from ipsum.tests.resources.data.model.ipsum_test_model import IpsumTestModel
from ipsum.util.enviroment_variable import get_test_database_url
from ipsum.util.test.database_test import DatabaseTest

class TestCRUDServices:

    TEST_DB_URI = get_test_database_url()

    dao = CRUDDAO(model=IpsumTestModel)

    crud_service = CRUDService(dao=dao, validator=CRUDValidator(dao), non_editable_fields=["code"])

    dao = crud_service._dao

    model = dao._model

    def test_insert(self):
        ipsum_test_model = IpsumTestModel(code=1, title='test_insert_TestDao')

        ipsum_database_test = DatabaseTest(host=self.TEST_DB_URI, daos_to_clean=[self.dao])
        def _():
            
            @ipsum_database_test.persistence_test()
            def test_insert_using_model():
                inserted_model = self.crud_service.insert(ipsum_test_model)
                db_model = self.model.objects().first()

                assert inserted_model.id == db_model.id
            test_insert_using_model()

            @ipsum_database_test.persistence_test()
            def test_insert_using_dict():
                model_dict = {
                    "code":2, "title":'test_insert_TestCRUDService'
                }

                inserted_model = self.crud_service.insert(model_dict)
                db_model = self.model.objects().first()

                assert inserted_model.code == db_model.code
            test_insert_using_dict()

        _()

    def test_delete(self):

        ipsum_test_model, ipsum_database_test = self._build_default_model_and_ipsum_test(1, 'test_delete_TestCRUDService')
        
        @ipsum_database_test.persistence_test()
        def _():
            ipsum_test_model_id = str(ipsum_test_model.id)

            deleted_id = self.crud_service.delete(ipsum_test_model_id)

            assert deleted_id == ipsum_test_model_id

            assert self.crud_service.find_by_id(ipsum_test_model_id) is None

            with raises(IpsumException, match=OBJECT_NOT_FOUND_EXCEPTION_MESSAGE.format(deleted_id)):
                self.crud_service.delete(deleted_id)

        _()

    def test_update(self):
        code = 1

        ipsum_test_model, ipsum_database_test = self._build_default_model_and_ipsum_test(code, 'test_update_TestCRUDService', True)

        @ipsum_database_test.persistence_test()
        def test_update_using_dict():
            model_id = ipsum_test_model.id 

            new_code = 2

            changes = {
                "title": "test_update_TestCRUDService Updated",
                "boolean": False,
	            "code": new_code,
            }

            updated_model = self.crud_service.update(model_id, changes)
            database_model = self.crud_service.find_by_id(model_id)

            assert updated_model.id == database_model.id == model_id
            assert updated_model.title == database_model.title == changes["title"]
            assert updated_model.boolean == database_model.boolean == changes["boolean"]
            assert code == updated_model.code == database_model.code != changes["code"]

        test_update_using_dict()

        ipsum_test_model, ipsum_database_test = self._build_default_model_and_ipsum_test(code, 'test_update_TestCRUDService', True)
        @ipsum_database_test.persistence_test()
        def test_update_using_model():
            model_id = ipsum_test_model.id 

            new_code = 2

            changes = ipsum_test_model
            changes.title = "test_update_TestDao Updated"
            changes.boolean = False 
            changes.code = new_code

            updated_model = self.crud_service.update(model_id, changes)
            database_model = self.crud_service.find_by_id(model_id)

            assert updated_model.id == database_model.id == model_id
            assert updated_model.title == database_model.title == changes.title
            assert updated_model.boolean == database_model.boolean == changes.boolean
            assert code == updated_model.code == database_model.code != new_code

        test_update_using_model()

    def test_must_remove_non_editable_fields(self):

        def test_remove_non_editable_fields_from_dict():

            title = "test_must_remove_non_editable_fields_TestNoteService"

            ipsum_test_model_dict = {
                "code": 1,
                "title": title,
                "boolean": True
            }

            editable_model = self.crud_service._remove_non_editable_fields_from_dict(ipsum_test_model_dict)

            assert "title" in editable_model
            assert "boolean" in editable_model

            for field in self.crud_service._non_editable_fields:
                assert field not in editable_model     

        test_remove_non_editable_fields_from_dict()

        code = 1
        ipsum_test_model, ipsum_database_test = self._build_default_model_and_ipsum_test(code, 'test_update_TestCRUDService', True)
        @ipsum_database_test.persistence_test()
        def test_remove_non_editable_fields_from_model():
            model_id = ipsum_test_model.id 

            new_code = 2

            changes = ipsum_test_model
            changes.title = "test_update_TestDao Updated"
            changes.boolean = False 
            changes.code = new_code

            changes = self.crud_service._remove_non_editable_fields_from_model(model_id, changes)

            assert ipsum_test_model.id == changes.id == model_id
            assert ipsum_test_model.title == changes.title == changes.title
            assert ipsum_test_model.boolean == changes.boolean == changes.boolean
            assert code == ipsum_test_model.code == changes.code != new_code            

        test_remove_non_editable_fields_from_model()

    def _build_default_model_and_ipsum_test(self, code, title, boolean=False):
        ipsum_test_model = IpsumTestModel(code=code, title=title, boolean=boolean)

        ipsum_database_test = DatabaseTest(host=self.TEST_DB_URI)
        ipsum_database_test.add_data(self.dao, ipsum_test_model)
        
        return ipsum_test_model, ipsum_database_test

    