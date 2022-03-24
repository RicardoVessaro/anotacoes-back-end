
class ArqService:

    def __init__(self, dao) -> None:
        self._dao = dao

    def insert(self, body: dict):
        return self._dao.insert(body)

    def delete(self, id):
        return self._dao.delete(id)   

    def find_by_id(self, id):
        return self._dao.find_by_id(id)

    def find(self, query_filter={}):
        return self._dao.find(query_filter)
        
    def paginate(self, query_filter={}, page=1, limit=5):
        return self._dao.paginate(query_filter=query_filter, page=page, limit=limit)



    