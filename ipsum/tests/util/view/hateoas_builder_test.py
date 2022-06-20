
import json
from this import d
from ipsum.util.data.pagination import Pagination
from ipsum.util.enviroment_variable import get_api_url
from ipsum.util.view.hateoas_builder import HATEOASBuilder
from ipsum.tests.resources.view.fake_crud_view import FakeCRUDView
from ipsum.tests.resources.view.fake_detail_crud_view import FakeDetailCRUDView
from ipsum.util.view.route_parser import parse_route
from ipsum.view.ipsum_view import DELETE, GET, PATCH, POST, QUERY_OFFSET

class TestHATEOASBuilder:

    HATEOAS_LINKS = '_links'

    host_url = 'http://localhost:5001/' 

    view_methods = [
        'insert', 'update', 'delete', 'find_by_id', 'find'
    ]

    PARENT_ID_PARAM = 'ipsum_model_id'
    PARENT_ID = '629fdb22fcce704dad685089'

    ID_PARAM = 'id'
    ID = '629fdb19fcce704dad685088'

    view_args = {PARENT_ID_PARAM: PARENT_ID, ID_PARAM: ID}

    def test_build_with_paginate(self):
        bytes_response = b'{"_items": [{"id": "62a6123275b113db96426022", "code": 1, "title": "test"}, {"id": "62a6125d75b113db96426023", "code": 2, "title": "other test"}, {"id": "62b0624f99edbc96b722a302", "code": 3, "title": "last test"}], "_info":{"limit": 2, "offset": 2, "total": 3, "empty": false} }'

        hateoas_builder = HATEOASBuilder(FakeCRUDView(), bytes_response, self.host_url, self.view_args, 'find', query_string='')
        self._assert_build(hateoas_builder, is_paginate=True)

        bytes_response = b'{"_items": [{"id": "62a6123275b113db96426022", "code": 1, "title": "test", "ipsum_model_id": "6248620366564103f229595f"}, {"id": "62a6125d75b113db96426023", "code": 2, "title": "other test", "ipsum_model_id": "629fdb22fcce704dad685089"}, {"id": "62b0624f99edbc96b722a302", "code": 3, "title": "last test", "ipsum_model_id": "62b0624f99edbc96b722a303"}], "_info":{"limit": 2, "offset": 2, "total": 3, "empty": false} }'

        hateoas_builder = HATEOASBuilder(FakeDetailCRUDView(), bytes_response, self.host_url, self.view_args, 'find', query_string='')
        self._assert_build(hateoas_builder, is_paginate=True)

    def test_build_with_list(self):

        bytes_response = b'[{\n "id": "62a505b437a970f7f060a0b2", \n  "code": "1", \n  "title": "test"\n}, {\n "id": "6248620366564103f229595f", \n  "code": "2", \n  "title": "other test"\n}]\n'
        hateoas_builder = HATEOASBuilder(FakeCRUDView(), bytes_response, self.host_url, self.view_args, 'list', query_string='')
        self._assert_build(hateoas_builder)

        bytes_response = b'[{\n "id": "629fdb19fcce704dad685088", \n  "code": "1", \n  "title": "test", \n  "ipsum_model_id": "629fdb22fcce704dad685089"\n}, {\n "id": "62a505b437a970f7f060a0b2", \n  "code": "1", \n  "title": "test", \n  "ipsum_model_id": "6248620366564103f229595f"\n}]\n'
        hateoas_builder = HATEOASBuilder(FakeDetailCRUDView(), bytes_response, self.host_url, self.view_args, 'list', query_string='')
        self._assert_build(hateoas_builder)

    def test_build_dict(self):
        bytes_response = b'{\n "id": "629fdb19fcce704dad685088", \n  "code": "1", \n  "title": "test"\n}\n'
        hateoas_builder = HATEOASBuilder(FakeCRUDView(), bytes_response, self.host_url, self.view_args, 'find_by_id', query_string='')
        self._assert_build(hateoas_builder)

        bytes_response = b'{\n "id": "629fdb19fcce704dad685088", \n  "code": "1", \n  "title": "test", \n  "ipsum_model_id": "629fdb22fcce704dad685089"\n}\n'
        hateoas_builder = HATEOASBuilder(FakeDetailCRUDView(), bytes_response, self.host_url, self.view_args, 'find_by_id', query_string='')
        self._assert_build(hateoas_builder)

    def test_is_paginate(self):
        item_data = {
            "_items": [
                {
                    "id": "62a6123275b113db96426022",
                    "code": 1,
                    "title": "test"
                },
                {
                    "id": "62a6125d75b113db96426023",
                    "code": 2,
                    "title": "other test"
                }
            ],
            "_info": {
                "offset": 0,
                "limit": 5,
                "total": 2,
                "empty": False
            }
        }

        hateoas_builder = HATEOASBuilder(FakeCRUDView(), {}, self.host_url, self.view_args, 'test', query_string='')

        assert True == hateoas_builder._is_paginate(item_data)

        item_data = {
            "id": "62a6125d75b113db96426023",
            "code": 2,
            "title": "other test"
        }
        assert False == hateoas_builder._is_paginate(item_data)

    def test_params_equals_params_in_view_rule(self):
        hateoas_builder = HATEOASBuilder(FakeCRUDView(), {}, self.host_url, self.view_args, 'test', query_string='')
        
        params = {
            self.ID_PARAM: self.ID,
            self.PARENT_ID_PARAM: self.PARENT_ID
        }
        view_rule = f'some/path<{self.PARENT_ID_PARAM}>/child/<{self.ID_PARAM}>'
        assert True == hateoas_builder._params_equals_params_in_view_rule(params, view_rule)

        params = {
            self.ID_PARAM: self.ID,
            self.PARENT_ID_PARAM: self.PARENT_ID
        }
        view_rule = f'some/path/<{self.ID_PARAM}>'
        assert False == hateoas_builder._params_equals_params_in_view_rule(params, view_rule)

        params = {
            self.ID_PARAM: self.ID,
        }
        view_rule = f'some/path/<{self.ID_PARAM}>'
        assert True == hateoas_builder._params_equals_params_in_view_rule(params, view_rule)

        params = {}
        view_rule = f'some/path/child'
        assert True == hateoas_builder._params_equals_params_in_view_rule(params, view_rule)


    def test_build_params(self):
        hateoas_builder = HATEOASBuilder(FakeCRUDView(), {}, self.host_url, self.view_args, 'test', query_string='')

        def _test_with_id_only():
            item_data = {self.ID_PARAM: self.ID, "code": "1", "title": "test"}

            expected_params = {self.ID_PARAM: self.ID}

            assert hateoas_builder._build_params(item_data) == expected_params
        _test_with_id_only()

        def _test_with_id_and_parent_id():
            item_data = {self.ID_PARAM: self.ID, "code": "1", "title": "test", self.PARENT_ID_PARAM: self.PARENT_ID}

            expected_params = {self.ID_PARAM: self.ID, self.PARENT_ID_PARAM: self.PARENT_ID}

            assert hateoas_builder._build_params(item_data) == expected_params
        _test_with_id_and_parent_id()

        def _test_with_empty_item_data():
            assert hateoas_builder._build_params({}) == self.view_args
        _test_with_empty_item_data()

        def _test_with_empty_view_args():
            _hateoas_builder = HATEOASBuilder(FakeCRUDView(), {}, self.host_url, {}, 'test', query_string='')
            
            item_data = {self.ID_PARAM: self.ID, "code": "1", "title": "test", self.PARENT_ID_PARAM: self.PARENT_ID}

            expected_params = {self.ID_PARAM: self.ID}

            assert _hateoas_builder._build_params(item_data) == expected_params
        _test_with_empty_view_args()

        def _test_with_empty_view_args_and_empty_item_data():
            _hateoas_builder = HATEOASBuilder(FakeCRUDView(), {}, self.host_url, {}, 'test', query_string='')

            assert _hateoas_builder._build_params({}) == {'id': None}
        _test_with_empty_view_args_and_empty_item_data()

        def _test_view_args_without_id():
            _hateoas_builder = HATEOASBuilder(FakeCRUDView(), {}, self.host_url, {self.PARENT_ID_PARAM: self.PARENT_ID}, 'test', query_string='')

            item_data = {self.ID_PARAM: self.ID, "code": "1", "title": "test", self.PARENT_ID_PARAM: self.PARENT_ID}

            expected_params = {self.ID_PARAM: self.ID, self.PARENT_ID_PARAM: self.PARENT_ID}

            assert _hateoas_builder._build_params(item_data) == expected_params
        _test_view_args_without_id()

    def test_get_response_data(self):

        hateoas_builder = HATEOASBuilder(FakeCRUDView(), {}, self.host_url, self.view_args, 'test', query_string='')

        def _test_with_bytes():

            bytes_response = b'{\n "id": "62a505b437a970f7f060a0b2", \n  "code": "1", \n  "title": "test"\n}\n'

            expected_response = {"id": "62a505b437a970f7f060a0b2", "code": "1", "title": "test"}

            hateoas_builder.response_data = bytes_response
            assert hateoas_builder.get_response_data() == expected_response

        _test_with_bytes()

        def _test_with_dict():
            dict_response = {"id": "62a505b437a970f7f060a0b2", "code": "1", "title": "test"}

            expected_response = {"id": "62a505b437a970f7f060a0b2", "code": "1", "title": "test"}

            hateoas_builder.response_data = dict_response
            assert hateoas_builder.get_response_data() == expected_response

        _test_with_dict()

        def _test_with_str():
            str_response = '{"id": "62a505b437a970f7f060a0b2", "code": "1", "title": "test"}'

            expected_response = {"id": "62a505b437a970f7f060a0b2", "code": "1", "title": "test"}

            hateoas_builder.response_data = str_response
            assert hateoas_builder.get_response_data() == expected_response

        _test_with_str()

        def _test_with_list_in_bytes():
            list_bytes_response = b'[{\n "id": "62a505b437a970f7f060a0b2", \n  "code": "1", \n  "title": "test"\n}, {\n "id": "6248620366564103f229595f", \n  "code": "2", \n  "title": "other test"\n}]\n'

            expected_response = [
                {"id": "62a505b437a970f7f060a0b2", "code": "1", "title": "test"},
                {"id": "6248620366564103f229595f", "code": "2", "title": "other test"}
            ]

            hateoas_builder.response_data = list_bytes_response
            assert hateoas_builder.get_response_data() == expected_response

        _test_with_list_in_bytes()

        def _test_with_empty_bytes():
            hateoas_builder.response_data = b''
            assert hateoas_builder.get_response_data() is None

        _test_with_empty_bytes()


    def test_is_text_response(self):
        hateoas_builder = HATEOASBuilder(FakeCRUDView(), {}, self.host_url, self.view_args, 'test', query_string='')

        assert False == hateoas_builder._is_text_response()

        hateoas_builder.response_data = 'str'
        assert True == hateoas_builder._is_text_response()

        hateoas_builder.response_data = b'bytes'
        assert True == hateoas_builder._is_text_response()


    def test_get_view_methods(self):

        def _assert(hateoas_builder):

            expected_view_methods = self.view_methods

            view_methods = hateoas_builder._get_view_methods()

            assert len(expected_view_methods) == len(view_methods)

            for view_method in view_methods:
                assert view_method in expected_view_methods

        _assert(HATEOASBuilder(FakeCRUDView(), {}, self.host_url, self.view_args, 'test', query_string=''))
        _assert(HATEOASBuilder(FakeDetailCRUDView(), {}, self.host_url, self.view_args, 'test', query_string=''))

    def test_get_rules(self):

        def _assert(hateoas_builder):
            expected_rules = {
                'insert': [''], 
                'update': ['<id>'], 
                'delete': ['<id>'], 
                'find_by_id': ['<id>'], 
                'find': [''], 
                'paginate': ['paginate']
            }

            for view_method in self.view_methods:
                assert expected_rules[view_method] == hateoas_builder._get_rules(view_method)

        _assert(HATEOASBuilder(FakeCRUDView(), {}, self.host_url, self.view_args, 'test', query_string=''))
        _assert(HATEOASBuilder(FakeDetailCRUDView(), {}, self.host_url, self.view_args, 'test', query_string=''))

    def test_get_actions(self):
        hateoas_builder = HATEOASBuilder(FakeCRUDView(), {}, self.host_url, self.view_args, 'test', query_string='')

        expected_actions = {
            'insert': [[POST]], 
            'update': [[PATCH]], 
            'delete': [[DELETE]], 
            'find_by_id': [[GET]], 
            'find': [[GET]], 
            'paginate': [[GET]]
        }

        for view_method in self.view_methods:
            assert expected_actions[view_method] == hateoas_builder._get_actions(view_method)

    def _assert_build(self, hateoas_builder, is_paginate=False):

        byte_data = hateoas_builder.build()

        data = json.loads(byte_data)

        if type(data) is list:
            for item_data in data:
                self._assert_build_item(hateoas_builder, item_data)  

        elif is_paginate:
            for item_data in data[Pagination.ITEMS]:
                self._assert_build_item(hateoas_builder, item_data, is_paginate, data[HATEOASBuilder.HATEOAS_LINKS], paginate_info=data[Pagination.INFO])  

        else:
            self._assert_build_item(hateoas_builder, item_data=data)

    def _assert_build_item(self, hateoas_builder, item_data, is_paginate=False, paginate_links=[], paginate_info=None):
        test_view = hateoas_builder.view

        links = item_data[self.HATEOAS_LINKS]

        parent_id = None
        if self.PARENT_ID_PARAM in item_data:
            parent_id = item_data[self.PARENT_ID_PARAM]

        id = item_data[self.ID_PARAM]

        expected_href = self._get_expected_href(test_view, parent_id=parent_id, id=id)
        expected_href_with_id = self._get_expected_href(test_view, with_id=True, parent_id=parent_id, id=id)

        response_data = hateoas_builder.get_response_data()

        if type(response_data) is list or is_paginate:

            if is_paginate:
                response_data = hateoas_builder.get_response_data()[Pagination.ITEMS]

            response_by_id = None
            for r in response_data:

                if r[self.ID_PARAM] == item_data[self.ID_PARAM]:
                    response_by_id = r

            response_data = response_by_id

        for key in item_data:
            if key != self.HATEOAS_LINKS:
                assert item_data[key] == response_data[key]

        expected_links = {
            'insert': {
                'name': 'insert',
                'rel': test_view.service.NAME,
                'href': expected_href,
                'action': [POST]
            },
            'update': {
                'name': 'update',
                'rel': test_view.service.NAME,
                'href': expected_href_with_id,
                'action': [PATCH]
            },
            'delete': {
                'name': 'delete',
                'rel': test_view.service.NAME,
                'href': expected_href_with_id,
                'action': [DELETE]
            },
            'find_by_id': {
                'name': 'find_by_id',
                'rel': test_view.service.NAME,
                'href': expected_href_with_id,
                'action': [GET]
            },
            'find': {
                'name': 'find',
                'rel': test_view.service.NAME,
                'href': expected_href,
                'action': [GET]
            },
            'paginate': {
                'name': 'paginate',
                'rel': test_view.service.NAME,
                'href': expected_href+'/paginate',
                'action': [GET]
            },
        }

        for link in links:
            name = link['name']

            assert name not in ['insert', 'find', 'paginate']

            assert link == expected_links[name]

        if is_paginate:

            for paginate_link in paginate_links:
                paginate_href = paginate_link['href']
                paginate_name = paginate_link['name']

                related_info = Pagination([]).related_info(paginate_info)

                for rel, info in related_info.items():
                    if rel == paginate_name:
                        assert f'{QUERY_OFFSET}={info[Pagination.OFFSET]}' in paginate_href

    def _get_expected_href(self, test_view, with_id=False, parent_id=None, id=None):
        _parent_id = parent_id if not parent_id is None else self.view_args[self.PARENT_ID_PARAM]

        _id = id if not id is None else self.view_args[self.ID_PARAM]

        formatted_route_prefix = f'{self.host_url}{test_view.route_prefix}'

        if self.PARENT_ID_PARAM in formatted_route_prefix:
            params = {
                self.PARENT_ID_PARAM: _parent_id
            }
            formatted_route_prefix = parse_route(formatted_route_prefix, params)

        formatted_route_prefix += test_view.route_base

        if with_id:
            formatted_route_prefix += f'/{_id}'

        return formatted_route_prefix
        


    