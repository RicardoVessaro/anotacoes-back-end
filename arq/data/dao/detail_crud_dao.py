
from xml.dom.minidom import Document
from arq.data.dao.crud_dao import CRUDDAO

class DetailCRUDDAO(CRUDDAO):

    def __init__(self, model: Document) -> None:
        super().__init__(model)

    def find(self, parent_id, **query_filter):
        query_filter[self._model.parent_field] = parent_id

        return super().find(**query_filter)

    def paginate(self, parent_id, page=1, limit=5, **query_filter) -> dict:
        query_filter[self._model.parent_field] = parent_id

        results = self.find(parent_id, **query_filter)

        return self._build_pagination(results, page, limit)