
from ipsum.exception.exception_message import PAGINATION_OFFSET_GREATER_THAN_TOTAL
from ipsum.exception.ipsum_exception import IpsumException
from ipsum.util.object_util import is_none_or_empty

class Pagination:

    ITEMS_KEY = "_items"
    INFO_KEY = "_info"

    def __init__(self, results, offset=0, limit=5) -> None:
        self.results = results
        self.offset = offset
        self.limit = limit


    def build(self):
        empty = is_none_or_empty(self.results)
        total = 0
        
        items = []
        if not empty:
            total = len(self.results)

            total_index = total - 1
            if self.offset > total_index:
                raise IpsumException(PAGINATION_OFFSET_GREATER_THAN_TOTAL.format("offset", self.offset, "total", total_index))

            _range = self.offset + self.limit
            items = self.results[self.offset:_range]

        pagination = {
            self.ITEMS_KEY: items,
            self.INFO_KEY: {
                "offset": self.offset,
                "limit": self.limit,
                "total": total,
                "empty": empty
            }
        }

        return pagination
