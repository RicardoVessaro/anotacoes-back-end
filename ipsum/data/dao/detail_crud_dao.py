
from xml.dom.minidom import Document
from ipsum.data.dao.crud_dao import CRUDDAO
from ipsum.exception.ipsum_exception import IpsumException
from ipsum.exception.exception_message import DETAIL_CRUD_DAO_MODEL_WITHOUT_PARENT_FIELD
from ipsum.util.object_util import is_none_or_empty

class DetailCRUDDAO(CRUDDAO):

    PARENT_FIELD = 'parent_field'

    def __init__(self, model: Document, cascade=None, dependent=None) -> None:
        self._validate_model_has_parent_field(model)

        super().__init__(
            model, 
            cascade=cascade,
            dependent=dependent
        )

    def find(self, parent_id, **query_filter):
        query_filter[self._model.parent_field] = parent_id

        return super().find(**query_filter)

    def paginate(self, parent_id, offset=0, limit=5, **query_filter) -> dict:
        query_filter[self._model.parent_field] = parent_id

        results = self.find(parent_id, **query_filter)

        return self._build_pagination(results, offset, limit)

    def _validate_model_has_parent_field(self, model):
        if not hasattr(model, self.PARENT_FIELD) or is_none_or_empty(model.parent_field):
            raise IpsumException(DETAIL_CRUD_DAO_MODEL_WITHOUT_PARENT_FIELD.format(model, DetailCRUDDAO.__class__, self.__class__, self.PARENT_FIELD))
