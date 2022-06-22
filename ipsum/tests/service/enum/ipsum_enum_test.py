
from pytest import raises
from ipsum.data.model.enum_document import CODE, NAME
from ipsum.exception.ipsum_exception import IpsumException
from ipsum.exception.exception_message import CLASS_MUST_BE_A_SUBCLASS_OF_ENUMSERVICE
from ipsum.service.enum.enum_service import EnumService
from ipsum.service.enum.ipsum_enum import ipsum_enum, enums_to_insert, EnumToInsert, save_enums
from ipsum.service.enum.enum_validator import EnumValidator
from ipsum.tests.resources.data.model.enum_test_model import EnumTestModel
from ipsum.data.dao.crud_dao import CRUDDAO
from ipsum.util.enviroment_variable import get_database_url
from ipsum.util.test.database_test import DatabaseTest


crud_dao = CRUDDAO(model=EnumTestModel)
enum_validator = EnumValidator(crud_dao, required_fields=[CODE, NAME])

enums_to_save = [
    EnumTestModel(code=0, name="ENUM 0"),
    EnumTestModel(code=1, name="ENUM 1"),
    EnumTestModel(code=2, name="ENUM 2"),
    EnumTestModel(code=3, name="ENUM 3"),
    EnumTestModel(code=4, name="ENUM 4"),
    EnumTestModel(code=5, name="ENUM 5")
]

@ipsum_enum()
class IpsumEnumService(EnumService):

    def __init__(self):
        enums = enums_to_save[0:3]
        
        super().__init__(
            dao=crud_dao, 
            validator=enum_validator,
            enums=enums
        )

@ipsum_enum(1, 'IpsumEnumServiceWithArgs', description="A Decorator Test", number=10)
class IpsumEnumServiceWithArgs(EnumService):
    
    def __init__(self, id, name, description=None, number=None):
        enums = enums_to_save[3:]
        
        super().__init__(
            dao=crud_dao, 
            validator=enum_validator, 
            enums=enums
        )

        self.id = id
        self.name = name
        self.description = description
        self.number = number


class TestIpsumEnum:

    TEST_DB_URI = get_database_url()

    def test_must_add_decorated_enums(self):

        IpsumEnumServiceToInsert = EnumToInsert(clazz=IpsumEnumService, args=(), kwargs={})
        IpsumEnumServiceWithArgsToInsert = EnumToInsert(
            clazz=IpsumEnumServiceWithArgs, args=(1, 'IpsumEnumServiceWithArgs'), 
            kwargs={'description':"A Decorator Test", 'number':10}
        )

        expected_enums = [IpsumEnumService, IpsumEnumServiceWithArgs]

        for e in enums_to_insert:
            e.clazz in expected_enums

            if e.clazz == IpsumEnumService:

                assert e.clazz == IpsumEnumServiceToInsert.clazz
                assert e.args == IpsumEnumServiceToInsert.args
                assert e.kwargs == IpsumEnumServiceToInsert.kwargs

            elif e.clazz == IpsumEnumServiceWithArgs:

                assert e.clazz == IpsumEnumServiceWithArgsToInsert.clazz
                assert e.args == IpsumEnumServiceWithArgsToInsert.args
                assert e.kwargs == IpsumEnumServiceWithArgsToInsert.kwargs

    def test_must_save_decorated_enums(self):
        
        database_test = DatabaseTest(host=self.TEST_DB_URI, daos_to_clean=[crud_dao])

        @database_test.persistence_test()
        def _():
            
            save_enums()
        
            for e in enums_to_save:
                result = crud_dao.find(code=e.code)

                assert not result is None

                db_enum = result.first()

                assert db_enum.code == e.code
                assert db_enum.name == e.name

        _()

    def test_must_raise_exception_when_decorated_enum_is_not_an_instance_of_enum_service(self):
        class ClazzToTest():
            pass 

        with raises(IpsumException, match=CLASS_MUST_BE_A_SUBCLASS_OF_ENUMSERVICE.format(ClazzToTest, EnumService)):
            ipsum_enum()(ClazzToTest)      

