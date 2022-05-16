
from xml.dom.minidom import Document
from arq.data.dao.crud_dao import CRUDDAO

class DetailCRUDDAO(CRUDDAO):

    def __init__(self, model: Document) -> None:
        super().__init__(model)

    def find_by_parent_id(self, parent_id, **query_filter):
        query_filter[self._model.parent_field] = parent_id

        return self.find(**query_filter)

    def paginate_by_parent_id(self, parent_id, page=1, limit=5, **query_filter):
        query_filter[self._model.parent_field] = parent_id

        return self.paginate(page, limit, **query_filter)