
from copy import copy
from datetime import datetime

import requests
from api.integration_tests.constants import NOTE_URL, TAG_URL
from ipsum.util.enviroment_variable import get_api_url
from ipsum.util.object_util import is_none_or_empty
from ipsum.util.test.view.crud_integration_test import CRUDIntegrationTest
from ipsum.util.test.view.view_integration_test import PaginateFilterResult
from ipsum.view.ipsum_view import ID, QUERY_LIMIT, QUERY_OFFSET, STATUS_CREATED, STATUS_OK


class TestNoteView(CRUDIntegrationTest):
    
    base_url = NOTE_URL

    body = {
        'title': 'Note Integration Test',
        'text': 'Loren ipsum dolor sit amet',
        'tag': '62dbd88ab6e09960b225c5ec',
        'moods': ['62dbd8e9b6e09960b225c5ed', '62dc062a3141aa4d53f507e3'],
        'pinned': True
    }

    update_body = {
        'title': 'Note Integration Test Update',
        'text': 'Loren ipsum dolor sit amet Update',
        'tag': '62a7b6988f048b47785281ef',
        'moods': ['62a7b6988f048b47785281e0', '62a7b6988f048b47785281f0'],
        'pinned': False
    }

    paginate_filter_results = [
        PaginateFilterResult(filter={}, expected_indexes=range(5), offset=0, limit=5, total=15, empty=False),
        PaginateFilterResult(filter={"pinned":False}, expected_indexes=range(8, 13), offset=0, limit=5, total=7, empty=False),
        PaginateFilterResult(filter={QUERY_LIMIT:7}, expected_indexes=range(7),  offset=0, limit=7, total=15, empty=False),
        PaginateFilterResult(filter={QUERY_OFFSET:5, QUERY_LIMIT:5},  expected_indexes=range(5,10), offset=5, limit=5, total=15, empty=False),
        PaginateFilterResult(filter={"pinned":False, QUERY_OFFSET:6, QUERY_LIMIT:6}, expected_indexes=[14], offset=6, limit=6, total=7, empty=False),
        PaginateFilterResult(filter={QUERY_OFFSET:14, QUERY_LIMIT:7},  expected_indexes=[14], offset=14, limit=7, total=15, empty=False)
    ]

    filter_to_not_found = {"title": "to not found"}

    def body_list(self):
        body_list = []

        pinned = True
        for i in range(15):

            body = {
                'title': f'{i} Note Integration Test',
                'text': 'Loren ipsum dolor sit amet',
                'tag': '62dbd88ab6e09960b225c5ec',
                'moods': ['62dbd8e9b6e09960b225c5ed', '62dc062a3141aa4d53f507e3'],
                'pinned': pinned
            }

            pinned = i < 7

            body_list.append(body)

        return body_list

    def test_insert(self):

        body = copy(self.body)
        body.pop('tag')
        body[ID] = '629fd999bcb136d8e94981ae'

        response = requests.post(self.url(), json=body)

        self.print_error(response)

        assert response.status_code == STATUS_CREATED

        self.print_error(response)

        response_body = response.json()

        for field in body:
            assert body[field] == response_body[field]

        assert 'created_in' in response_body
        assert not is_none_or_empty(response_body['created_in'])
        assert self.isoformat_date(response_body['created_in']) == datetime.today().date().isoformat()

        assert 'tag' in response_body
        assert not is_none_or_empty(response_body['tag'])

        TAG_OK_CODE = '2'
        tag_url = f'{get_api_url()}/{TAG_URL}?code={TAG_OK_CODE}'
        tag_response = requests.get(tag_url)

        tag_body = tag_response.json()
        tag_id = tag_body['_items'][0][ID]

        assert tag_id == response_body['tag']

        url = f'{self.url()}/{body[ID]}'
        requests.delete(url)

    def isoformat_date(self, isoformat_date):
        return isoformat_date.split('T')[0]
