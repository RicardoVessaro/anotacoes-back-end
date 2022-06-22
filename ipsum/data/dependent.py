
from collections import namedtuple
from bson import ObjectId
from ipsum.data.dao.dao import DAO
from ipsum.exception.exception_message import DEPENDENCY_DAO_IS_NOT_DAO_TYPE, DEPENDENT_DEPENDENCY_HAS_DATA, DEPENDENT_DEPENDENCY_IS_NOT_DEPENDENCY_TYPE

from ipsum.exception.ipsum_exception import IpsumException

class Dependent:

    DEPENDENCY_DAO_ATTRIBUTE = "dao"

    Dependency = namedtuple('Dependency', f'{DEPENDENCY_DAO_ATTRIBUTE} name dependency_field')

    DEPENDENTS_ATTRIBUTE = "dependents"

    def __init__(self, name, dependents) -> None:
        self.name = name
        self.dependents = dependents

        self._validate_dependents_type()

    def check_dependents_data(self, id):

        _id = id 

        if type(id) is str:
            _id = ObjectId(id)

        for dependent in self.dependents:

            model = dependent.dao.model

            query_filter = {dependent.dependency_field: _id}

            result = model.objects(**query_filter).first()

            model_has_data = result is not None

            if model_has_data:
                raise IpsumException(DEPENDENT_DEPENDENCY_HAS_DATA.format(self.name, str(_id), dependent.name, result.id))

    def _validate_dependents_type(self):
        for dependent in self.dependents:

            if not isinstance(dependent, Dependent.Dependency):
                raise IpsumException(DEPENDENT_DEPENDENCY_IS_NOT_DEPENDENCY_TYPE.format(self.DEPENDENTS_ATTRIBUTE, self.__class__, Dependent.Dependency, dependent.__class__))

            if not isinstance(dependent.dao, DAO):
                raise IpsumException(DEPENDENCY_DAO_IS_NOT_DAO_TYPE.format(self.DEPENDENCY_DAO_ATTRIBUTE, dependent.__class__, DAO, dependent.dao.__class__))
        
        