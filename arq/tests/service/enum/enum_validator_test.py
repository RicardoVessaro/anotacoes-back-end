
from pytest import raises
from arq.data.dao.crud_dao import CRUDDAO
from arq.data.model.enum_document import CODE, NAME
from arq.exception.exception_message import DUPLICATED_ENUM_CODE, REQUIRED_FIELD_EXCEPTION_MESSAGE
from arq.service.enum.enum_validator import EnumValidator
from arq.tests.resources.data.model.enum_test_model import EnumTestModel
from arq.exception.arq_exception import ArqException
from arq.util.test.database_test import DatabaseTest

class TestEnumValidator:

    TEST_DB_URI = "mongodb+srv://user:senha@anotacoes-cluster.jwtdf.mongodb.net/anotacoes-test?retryWrites=true&w=majority"

    enum_validator = EnumValidator(dao=CRUDDAO(model=EnumTestModel))

    dao = enum_validator._dao

    # TDD EnumValidator

    def test_duplicated_enum_codes(self):
        database_test = DatabaseTest(daos_to_clean=[self.dao])

        @database_test.persistence_test(host=self.TEST_DB_URI)
        def _must_raise_exception_when_code_is_duplicated():

            enums = [
                EnumTestModel(code=1, name='Test 1', integer=10),
                EnumTestModel(code=2, name='Test 2', integer=20),
                EnumTestModel(code=3, name='Test 3', integer=30),
                EnumTestModel(code=2, name='Test 4', integer=40),
            ]

            with raises(ArqException, match=DUPLICATED_ENUM_CODE.format(2)):
                self.enum_validator.validate_enums(enums)

        _must_raise_exception_when_code_is_duplicated()

        @database_test.persistence_test(host=self.TEST_DB_URI)
        def _must_not_raise_exception():
            
            enums = [
                EnumTestModel(code=1, name='Test 1', integer=10),
                EnumTestModel(code=2, name='Test 2', integer=20),
                EnumTestModel(code=3, name='Test 3', integer=30),
                EnumTestModel(code=4, name='Test 4', integer=40),
            ]

            self.enum_validator.validate_enums(enums)

        _must_not_raise_exception()
