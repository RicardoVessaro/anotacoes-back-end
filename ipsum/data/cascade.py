
from ipsum.data.dao.detail_crud_dao import DetailCRUDDAO
from ipsum.exception.exception_message import CASCADE_CHILDS_MUST_BE_INSTANCE_OF_DAO
from ipsum.exception.ipsum_exception import IpsumException


class Cascade:
    
    DAO_ATTRIBUTE = "childs"

    def __init__(self, childs) -> None:
        self._childs = childs

        self._validate_childs_type()

    @property
    def childs(self):
        return self._childs

    def delete(self, parent_id):
        return self._delete(self.childs, parent_id)

    def _delete(self, childs, parent_id):
        for dao in childs:
            data = dao.find(parent_id)

            dao.delete(data)

    def _validate_childs_type(self):

        for child in self.childs:
            if not isinstance(child, DetailCRUDDAO):
                raise IpsumException(CASCADE_CHILDS_MUST_BE_INSTANCE_OF_DAO.format(Cascade, self.DAO_ATTRIBUTE, DetailCRUDDAO, child.__class__))


    