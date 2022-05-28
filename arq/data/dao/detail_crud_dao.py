
from xml.dom.minidom import Document
from arq.data.dao.crud_dao import CRUDDAO
from arq.exception.arq_exception import ArqException
from arq.exception.exception_message import DETAIL_CRUD_DAO_MODEL_WITHOUT_PARENT_FIELD
from arq.util.object_util import is_none_or_empty

class DetailCRUDDAO(CRUDDAO):

    PARENT_FIELD = 'parent_field'

    def __init__(self, model: Document) -> None:
        if not hasattr(model, self.PARENT_FIELD) or is_none_or_empty(model.parent_field):
            raise ArqException(DETAIL_CRUD_DAO_MODEL_WITHOUT_PARENT_FIELD.format(model, DetailCRUDDAO.__class__, self.__class__, self.PARENT_FIELD))

        super().__init__(model)

    def find(self, parent_id, **query_filter):
        query_filter[self._model.parent_field] = parent_id

        return super().find(**query_filter)

    def paginate(self, parent_id, page=1, limit=5, **query_filter) -> dict:
        query_filter[self._model.parent_field] = parent_id

        results = self.find(parent_id, **query_filter)

        return self._build_pagination(results, page, limit)