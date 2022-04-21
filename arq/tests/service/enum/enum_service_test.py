
from pytest import raises
from arq.data.model.enum_document import CODE, NAME
from arq.exception.arq_exception import ArqException
from arq.exception.exception_message import REQUIRED_FIELD_EXCEPTION_MESSAGE
from arq.service.enum.enum_service import EnumService
from arq.data.dao.crud_dao import CRUDDAO
from arq.tests.resources.data.model.enum_test_model import EnumTestModel
from arq.service.enum.enum_validator import EnumValidator
from arq.util.enviroment_variable import get_test_database_url
from arq.util.test.database_test import DatabaseTest

class TestEnumService:

    TEST_DB_URI = get_test_database_url()

    def test_must_raise_exception_when_required_field_is_none_on_insert(self):

        def _test_code_is_empty():

            enums = [EnumTestModel(code=None, name="Test", integer=10)]

            enum_service = self._get_enum_service(enums)

            database_test = DatabaseTest(daos_to_clean=[enum_service._dao])
            @database_test.persistence_test(host=self.TEST_DB_URI)
            def _():
                with raises(ArqException, match=REQUIRED_FIELD_EXCEPTION_MESSAGE.format(CODE)):
                    enum_service.save_enums()
            _()
        
        _test_code_is_empty()

        def _test_name_is_empty():
                enums = [EnumTestModel(code=1, name=None, integer=10)]

                enum_service = self._get_enum_service(enums)

                database_test = DatabaseTest(daos_to_clean=[enum_service._dao])
                @database_test.persistence_test(host=self.TEST_DB_URI)
                def _():

                    with raises(ArqException, match=REQUIRED_FIELD_EXCEPTION_MESSAGE.format(NAME)):
                        enum_service.save_enums()

                _()
        
        _test_name_is_empty()

        def _test_integer_is_empty():

                INTEGER = 'integer'

                enums = [EnumTestModel(code=1, name='Test', integer=None)]

                enum_service = self._get_enum_service(enums, required_fields=[INTEGER])

                database_test = DatabaseTest(daos_to_clean=[enum_service._dao])
                @database_test.persistence_test(host=self.TEST_DB_URI)
                def _():

                    with raises(ArqException, match=REQUIRED_FIELD_EXCEPTION_MESSAGE.format(INTEGER)):
                        enum_service.save_enums()
                _()
        
        _test_integer_is_empty()

        
        def _test_no_exception():

                enums = [EnumTestModel(code=1, name='Test', integer=None)]

                enum_service = self._get_enum_service(enums)

                database_test = DatabaseTest(daos_to_clean=[enum_service._dao])
                @database_test.persistence_test(host=self.TEST_DB_URI)
                def _():

                    enum_service.save_enums()
                _()
        
        _test_no_exception()


    
    def test_must_raise_exception_when_required_field_is_none_on_update(self):

        def _test_code_is_empty():

                enums = [EnumTestModel(code=None, name="Test DEBUG", integer=10)]
                enum_service = self._get_enum_service(enums)

                db_enum = EnumTestModel(code=1, name="Test", integer=10)
                database_test = DatabaseTest()
                database_test.add_data(enum_service._dao, db_enum)
                
                @database_test.persistence_test(host=self.TEST_DB_URI)
                def _():
                    with raises(ArqException, match=REQUIRED_FIELD_EXCEPTION_MESSAGE.format(CODE)):
                        enum_service.save_enums()
                _()
        
        _test_code_is_empty()

        def _test_name_is_empty():
                enums = [EnumTestModel(code=1, name=None, integer=10)]

                enum_service = self._get_enum_service(enums)

                db_enum = EnumTestModel(code=1, name="Test", integer=10)
                database_test = DatabaseTest()
                database_test.add_data(enum_service._dao, db_enum)
                
                @database_test.persistence_test(host=self.TEST_DB_URI)
                def _():

                    with raises(ArqException, match=REQUIRED_FIELD_EXCEPTION_MESSAGE.format(NAME)):
                        enum_service.save_enums()

                _()
        
        _test_name_is_empty()

        def _test_integer_is_empty():

                INTEGER = 'integer'

                enums = [EnumTestModel(code=1, name='Test', integer=None)]

                enum_service = self._get_enum_service(enums, required_fields=[INTEGER])

                db_enum = EnumTestModel(code=1, name="Test", integer=10)
                database_test = DatabaseTest()
                database_test.add_data(enum_service._dao, db_enum)
                
                @database_test.persistence_test(host=self.TEST_DB_URI)
                def _():
                    with raises(ArqException, match=REQUIRED_FIELD_EXCEPTION_MESSAGE.format(INTEGER)):
                        enum_service.save_enums()
                _()
        
        _test_integer_is_empty()

        def _test_no_exception():

                enums = [EnumTestModel(code=1, name='Test', integer=None)]

                enum_service = self._get_enum_service(enums)

                db_enum = EnumTestModel(code=1, name="Test", integer=10)
                database_test = DatabaseTest()
                database_test.add_data(enum_service._dao, db_enum)
                
                @database_test.persistence_test(host=self.TEST_DB_URI)
                def _():
                    enum_service.save_enums()
                _()
        
        _test_no_exception()


    def test_must_save_enums(self):
        enums = [
            EnumTestModel(code=1, name='Test 1', integer=10),
            EnumTestModel(code=2, name='Test 2', integer=20),
            EnumTestModel(code=3, name='Test 3', integer=30),
        ]

        enum_service = self._get_enum_service(enums)
        database_test = DatabaseTest(daos_to_clean=[enum_service._dao])

        @database_test.persistence_test(host=self.TEST_DB_URI)
        def _():
            enum_service.save_enums()

            for enum in enums:
                db_enum = enum_service.find(code=enum.code).first()

                assert db_enum is not None
                assert enum.id == db_enum.id
                assert enum.code == db_enum.code
                assert enum.name == db_enum.name
                assert enum.integer == db_enum.integer
        _()

    def test_must_update_enums(self):
        enums = [
            EnumTestModel(code=1, name='Test 1', integer=10),
            EnumTestModel(code=2, name='Test 2', integer=20),
            EnumTestModel(code=3, name='Test 3', integer=30),
        ]

        enum_service = self._get_enum_service(enums)

        database_test = DatabaseTest()
        database_test.add_data(enum_service._dao, enums)

        @database_test.persistence_test(host=self.TEST_DB_URI)
        def _():
            enum_service.enums[1].name = 'Test 2 Updated'
            enum_service.enums[1].integer = 200

            enum_service.enums[2].name = 'Test 3 Updated'
            enum_service.enums[2].integer = 300

            enum_service.enums.append(EnumTestModel(code=4, name='Test 4', integer=40))

            enum_service.save_enums()

            for enum in enum_service.enums:
                db_enum = enum_service.find(code=enum.code).first()

                assert db_enum is not None
                assert enum.id == db_enum.id
                assert enum.code == db_enum.code
                assert enum.name == db_enum.name
                assert enum.integer == db_enum.integer
        _()

    def _get_enum_service(self, enums, required_fields=[]) -> EnumService:
        dao = CRUDDAO(model=EnumTestModel)

        enum_service = EnumService(
            dao=dao,
            validator=EnumValidator(dao=dao, required_fields=required_fields),
            enums=enums
        )

        return enum_service