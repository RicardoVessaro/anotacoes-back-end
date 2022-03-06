

class ArqService:

    def __init__(self, dao, validator, non_editable_fields=[]) -> None:
        self._dao = dao
        self._validator = validator
        self._non_editable_fields = non_editable_fields

    def find_by_id(self, id):
        return self._dao.find_by_id(id)

    def find(self, query_filter={}):
        return self._dao.find(query_filter)
        
    def paginate(self, query_filter={}, page=1, limit=5):
        return self._dao.paginate(query_filter=query_filter, page=page, limit=limit)



    