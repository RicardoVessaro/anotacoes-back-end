
from unittest.mock import patch
from pytest import raises
from bson import ObjectId
from ipsum.data.dao.dao import DAO 
from ipsum.data.dependent import Dependent
from ipsum.exception.exception_message import DEPENDENCY_DAO_IS_NOT_DAO_TYPE, DEPENDENT_DEPENDENCY_HAS_DATA, DEPENDENT_DEPENDENCY_IS_NOT_DEPENDENCY_TYPE
from ipsum.exception.ipsum_exception import IpsumException
from ipsum.tests.resources.data.model.ipsum_test_model import IpsumTestModel
from ipsum.util.enviroment_variable import get_database_url
from ipsum.util.test.database_test import DatabaseTest

class TestDependent:

    TEST_DATABASE_URL = get_database_url()

    def test_validate_dependents_type(self):

        class DependentDAO(DAO):
            pass

        class CustomDependency(Dependent.Dependency):
            pass

        class NotDependency():
            pass

        dependency = Dependent.Dependency(DependentDAO(IpsumTestModel), 'Dependent DAO', 'field')

        custom_dependency = CustomDependency(DependentDAO(IpsumTestModel), 'Custom Dependency', 'field')

        not_dependency = NotDependency()

        with raises(IpsumException, match=DEPENDENT_DEPENDENCY_IS_NOT_DEPENDENCY_TYPE.format(Dependent.DEPENDENTS_ATTRIBUTE, Dependent, Dependent.Dependency, NotDependency)):
            Dependent('dependent', dependents=[dependency, custom_dependency, not_dependency])

    def test_validate_dependency_dao_type(self):

        class DependentDAO(DAO):
            pass

        class CustomDependency(Dependent.Dependency):
            pass

        class NotDAO():
            pass

        dependency = Dependent.Dependency(DependentDAO(IpsumTestModel), 'Dependent DAO', 'field')

        custom_dependency = CustomDependency(DependentDAO(IpsumTestModel), 'Custom Dependency', 'field')

        dependency_not_dao = Dependent.Dependency(NotDAO(), 'Not DAO', 'field')

        with raises(IpsumException, match=DEPENDENCY_DAO_IS_NOT_DAO_TYPE.format(Dependent.DEPENDENCY_DAO_ATTRIBUTE, Dependent.Dependency, DAO, NotDAO)):
            Dependent('dependent', dependents=[dependency, custom_dependency, dependency_not_dao])

    def test_must_not_raise_exception_when_not_exists_data(self):

        database_test = DatabaseTest(host=self.TEST_DATABASE_URL)
        @database_test.persistence_test()
        def _():

            dependency = Dependent.Dependency(DAO(IpsumTestModel), 'DAO', 'dependency_id')

            dependent = Dependent('dependent', dependents=[dependency])

            dependent.check_dependents_data(ObjectId())

        _()

    def test_must_raise_exception_when_exists_data(self):

        dependency_id = str(ObjectId())
        
        dao = DAO(IpsumTestModel)
        model = dao.model(code=1, dependency_id=dependency_id)

        database_test = DatabaseTest(host=self.TEST_DATABASE_URL)
        database_test.add_data(dao, model)

        @database_test.persistence_test()
        def _():

            dependency = Dependent.Dependency(dao, 'DAO', 'dependency_id')

            dependent = Dependent('dependent', dependents=[dependency])

            with raises(IpsumException, match=DEPENDENT_DEPENDENCY_HAS_DATA.format(dependent.name, dependency_id, dependency.name, model.id)):
                dependent.check_dependents_data(dependency_id)

        _()

    def test_must_not_raise_exception_when_exists_data_with_diferent_id(self):

        dependency_id = str(ObjectId())

        other_id = str(ObjectId())
        
        dao = DAO(IpsumTestModel)
        model = dao.model(code=1, dependency_id=dependency_id)

        database_test = DatabaseTest(host=self.TEST_DATABASE_URL)
        database_test.add_data(dao, model)

        @database_test.persistence_test()
        def _():

            dependency = Dependent.Dependency(dao, 'DAO', 'dependency_id')

            dependent = Dependent('dependent', dependents=[dependency])

            dependent.check_dependents_data(other_id)

        _()
