
from abc import ABC, abstractmethod, abstractproperty
from collections import namedtuple

import requests
from ipsum.exception.exception_message import PAGINATION_OFFSET_GREATER_THAN_TOTAL
from ipsum.util.data.pagination import Pagination
from ipsum.util.enviroment_variable import get_api_url
from ipsum.util.object_util import is_none_or_empty

from ipsum.util.test.integration_test import  IntegrationTest
from ipsum.view.ipsum_view import ID, STATUS_BAD_REQUEST, STATUS_NO_CONTENT, STATUS_OK

ID_FIELD = 'id'

PaginateFilterResult = namedtuple('PaginateFilterResult', f'filter expected_indexes {Pagination.OFFSET} {Pagination.LIMIT} {Pagination.TOTAL} {Pagination.EMPTY}')

class ViewIntegrationTest(ABC):

    @abstractproperty
    def base_url(self):
        pass

    @abstractproperty
    def paginate_filter_results(self):
        pass

    @abstractproperty
    def filter_to_not_found(self):
        pass

    @abstractmethod
    def body_list(self):
        pass

    @abstractmethod
    def test_find_by_id(self):
        pass

    @abstractmethod
    def test_find(self):
        pass

    def assert_find(self, body_list):
        self._assert_body_list(body_list)
        self._assert_must_return_empty_when_not_found_in_filter(body_list)
        self._assert_must_return_400_bad_request_when_when_offset_is_greater_than_total(body_list)

    def url(self):
        return f'{get_api_url()}/{self.base_url}'

    def _assert_body_list(self, body_list):
        for paginate_filter_result in self.paginate_filter_results:
            response = requests.get(self.url(), params=paginate_filter_result.filter)

            self.print_error(response)
            assert response.status_code == STATUS_OK

            items = response.json()

            pagination_info = items[Pagination.INFO]

            assert pagination_info[Pagination.OFFSET] == paginate_filter_result.offset
            assert pagination_info[Pagination.LIMIT] == paginate_filter_result.limit
            assert pagination_info[Pagination.TOTAL] == paginate_filter_result.total
            assert pagination_info[Pagination.EMPTY] == paginate_filter_result.empty

            expected_ids = self._get_expected_ids(
                paginate_filter_result.expected_indexes, body_list)

            pagination_item = items[Pagination.ITEMS]

            assert len(pagination_item) == len(expected_ids)

            for item in pagination_item:
                assert item[ID_FIELD] in expected_ids

    def _assert_must_return_empty_when_not_found_in_filter(self, body_list):
        response = requests.get(self.url(), params=self.filter_to_not_found)
        
        self.print_error(response)

        assert response.status_code == STATUS_OK

        items = response.json()

        pagination_info = items[Pagination.INFO]

        offset = 0
        if Pagination.OFFSET in self.filter_to_not_found:
            offset = self.filter_to_not_found[Pagination.OFFSET]

        limit = 5
        if Pagination.LIMIT in self.filter_to_not_found:
            limit = self.filter_to_not_found[Pagination.LIMIT]

        assert pagination_info[Pagination.OFFSET] == offset
        assert pagination_info[Pagination.LIMIT] == limit
        assert pagination_info[Pagination.TOTAL] == 0
        assert pagination_info[Pagination.EMPTY] == True
        assert is_none_or_empty(items[Pagination.ITEMS]) 

    def _assert_must_return_400_bad_request_when_when_offset_is_greater_than_total(self, body_list):
        offset = self._get_body_list_length(body_list) 

        response = requests.get(self.url(), params={"_limit":1, "_offset": offset })

        self.print_error(response)

        assert response.status_code == STATUS_BAD_REQUEST

        items = response.json()

        total_index = offset - 1

        assert items['message'] == PAGINATION_OFFSET_GREATER_THAN_TOTAL.format(Pagination.OFFSET, offset, Pagination.TOTAL, total_index)
        assert items['status_code'] == STATUS_BAD_REQUEST

    def _get_expected_ids(self, indexes, body_list):
        expected_ids = []
        for index in indexes:
            id = body_list[index][ID]
            expected_ids.append(id)

        return expected_ids

    def _get_body_list_length(self, body_list):
        body_list_length = len(body_list)

        return body_list_length

    def print_error(self, response):
        if response.status_code == 400:
                item = response.json()
                print('\n', item['message'])

