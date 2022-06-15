
from abc import abstractproperty

class Service:

    fields_inserted_by_default = None
    
    @abstractproperty
    def NAME(self):
        pass

    def __init__(self, dao) -> None:
        self._dao = dao

    @property
    def dao(self):
        return self._dao

    def insert(self, body: dict, **kwargs):
        return self._dao.insert(body, **kwargs)

    def delete(self, id):
        return self._dao.delete(id)   

    def find_by_id(self, id):
        return self._dao.find_by_id(id)

    def find(self, **query_filter):
        return self._dao.find(**query_filter)
        
    def paginate(self, offset=0, limit=5, **query_filter):
        return self._dao.paginate(offset=offset, limit=limit, **query_filter)
    