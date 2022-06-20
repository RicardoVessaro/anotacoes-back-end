
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

    SELF = "self"
    NEXT = "next"
    PREVIOUS = "previous"
    FIRST = "first"
    LAST = "last"

    KEYS = [
        ITEMS, INFO
    ]

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

    def related_info(self, info):

        empty = info[self.EMPTY]
        offset = info[self.OFFSET]
        limit = info[self.LIMIT]
        total = info[self.TOTAL]

        if empty:
            return {
                self.SELF: self._build_related_dict(limit, offset),
                self.NEXT: None,
                self.PREVIOUS: None,
                self.FIRST: None,
                self.LAST: None
            }

        return {
            self.SELF: self._build_related_dict(limit, offset),
            self.NEXT: self._next_rel(offset, limit, total),
            self.PREVIOUS: self._previous_rel(offset, limit),
            self.FIRST: self._first_rel(offset, limit),
            self.LAST: self._last_rel(offset, limit, total)
        }

    def _last_rel(self, offset, limit, total):
        intervals = total // limit
        last_offset = intervals * limit

        interval_mod = total % limit
        if interval_mod == 0:
            last_offset -= limit

        if last_offset != offset:
            return self._build_related_dict(limit, last_offset)

        return None

    def _first_rel(self, offset, limit):
        first_offset = 0
        if first_offset != offset:
            return self._build_related_dict(limit, first_offset)

        return None

    def _previous_rel(self, offset, limit):
        previous_offset = offset - limit
        if previous_offset >= 0:
            return self._build_related_dict(limit, previous_offset)
        
        return None

    def _next_rel(self, offset, limit, total):

        next_offset = offset + limit
        if next_offset < total:
            return self._build_related_dict(limit, next_offset)

        return None

    def _build_related_dict(self, limit, offset):
        return {
            self.LIMIT: limit,
            self.OFFSET: offset
        }
