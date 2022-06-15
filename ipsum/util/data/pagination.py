
from ipsum.exception.exception_message import PAGINATION_OFFSET_GREATER_THAN_TOTAL
from ipsum.exception.ipsum_exception import IpsumException
from ipsum.util.object_util import is_none_or_empty

class Pagination:

    ITEMS = "_items"
    INFO = "_info"
    OFFSET = "offset"
    LIMIT = "limit"
    TOTAL = "total"
    EMPTY = "empty"

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
                raise IpsumException(PAGINATION_OFFSET_GREATER_THAN_TOTAL.format(self.OFFSET, self.offset, self.TOTAL, total_index))

            _range = self.offset + self.limit
            items = self.results[self.offset:_range]

        pagination = {
            self.ITEMS: items,
            self.INFO: {
                self.OFFSET: self.offset,
                self.LIMIT: self.limit,
                self.TOTAL: total,
                self.EMPTY: empty
            }
        }

        return pagination
