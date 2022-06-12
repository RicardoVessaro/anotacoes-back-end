
import json
from this import d
from ipsum.util.enviroment_variable import get_api_url
from ipsum.util.view.hateoas_builder import HATEOASBuilder
from ipsum.tests.resources.view.fake_crud_view import FakeCRUDView
from ipsum.tests.resources.view.fake_detail_crud_view import FakeDetailCRUDView
from ipsum.util.view.route_parser import parse_route
from ipsum.view.ipsum_view import DELETE, GET, PATCH, POST

# python3 -m pytest -p no:cacheprovider --capture=no ipsum/tests/util/view/hateoas_builder_test.py

class TestHATEOASBuilder:

    host_url = 'http://localhost:5001/' 

    view_methods = [
        'insert', 'update', 'delete', 'find_by_id', 'find', 'paginate'
    ]

    PARENT_ID_PARAM = 'ipsum_model_id'
    PARENT_ID = '629fdb22fcce704dad685089'

    ID_PARAM = 'id'
    ID = '629fdb19fcce704dad685088'

    view_args = {PARENT_ID_PARAM: PARENT_ID, ID_PARAM: ID}

    def test_build(self):

        def _assert(test_view, bytes_response):

            hateoas_builder = HATEOASBuilder(test_view, bytes_response, self.host_url, self.view_args)

            byte_data = hateoas_builder.build()

            data = json.loads(byte_data)

            links = data['_links']

            expected_href = self._get_expected_href(test_view)
            expected_href_with_id = self._get_expected_href(test_view, with_id=True)

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
                    'action': [POST]
                },
            }

            for link in links:
                name = link['name']
                assert link == expected_links[name]

        # TODO usar variaveis no id (ainda naoo usadoo por causa dos bytes)
        bytes_response = b'{\n "id": "629fdb19fcce704dad685088", \n  "code": "1", \n  "title": "test"\n}\n'
        _assert(FakeCRUDView(), bytes_response)

        bytes_response = b'{\n "id": "629fdb19fcce704dad685088", \n  "code": "1", \n  "title": "test", \n  "ipsum_model_id": "629fdb22fcce704dad685089"\n}\n'
        _assert(FakeDetailCRUDView(), bytes_response)

    def test_build_params(self):
        hateoas_builder = HATEOASBuilder(FakeCRUDView(), {}, self.host_url, self.view_args)

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
            _hateoas_builder = HATEOASBuilder(FakeCRUDView(), {}, self.host_url, {})
            
            item_data = {self.ID_PARAM: self.ID, "code": "1", "title": "test", self.PARENT_ID_PARAM: self.PARENT_ID}

            expected_params = {self.ID_PARAM: self.ID}

            assert _hateoas_builder._build_params(item_data) == expected_params
        _test_with_empty_view_args()

        def _test_with_empty_view_args_and_empty_item_data():
            _hateoas_builder = HATEOASBuilder(FakeCRUDView(), {}, self.host_url, {})

            assert _hateoas_builder._build_params({}) == {'id': None}
        _test_with_empty_view_args_and_empty_item_data()

        def _test_view_args_without_id():
            _hateoas_builder = HATEOASBuilder(FakeCRUDView(), {}, self.host_url, {self.PARENT_ID_PARAM: self.PARENT_ID})

            item_data = {self.ID_PARAM: self.ID, "code": "1", "title": "test", self.PARENT_ID_PARAM: self.PARENT_ID}

            expected_params = {self.ID_PARAM: self.ID, self.PARENT_ID_PARAM: self.PARENT_ID}

            assert _hateoas_builder._build_params(item_data) == expected_params
        _test_view_args_without_id()

    def test_get_response_data(self):

        hateoas_builder = HATEOASBuilder(FakeCRUDView(), {}, self.host_url, self.view_args)

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
        hateoas_builder = HATEOASBuilder(FakeCRUDView(), {}, self.host_url, self.view_args)

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

        _assert(HATEOASBuilder(FakeCRUDView(), {}, self.host_url, self.view_args))
        _assert(HATEOASBuilder(FakeDetailCRUDView(), {}, self.host_url, self.view_args))

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

        _assert(HATEOASBuilder(FakeCRUDView(), {}, self.host_url, self.view_args))
        _assert(HATEOASBuilder(FakeDetailCRUDView(), {}, self.host_url, self.view_args))

    def test_get_actions(self):
        hateoas_builder = HATEOASBuilder(FakeCRUDView(), {}, self.host_url, self.view_args)

        expected_actions = {
            'insert': [[POST]], 
            'update': [[PATCH]], 
            'delete': [[DELETE]], 
            'find_by_id': [[GET]], 
            'find': [[GET]], 
            'paginate': [[POST]]
        }

        for view_method in self.view_methods:
            assert expected_actions[view_method] == hateoas_builder._get_actions(view_method)

    def _get_expected_href(self, test_view, with_id=False):
        formatted_route_prefix = f'{self.host_url}{test_view.route_prefix}'

        if self.PARENT_ID_PARAM in formatted_route_prefix:
            params = {
                self.PARENT_ID_PARAM: self.view_args[self.PARENT_ID_PARAM]
            }
            formatted_route_prefix = parse_route(formatted_route_prefix, params)

        formatted_route_prefix += test_view.route_base

        if with_id:
            formatted_route_prefix += f'/{self.view_args[self.ID_PARAM]}'

        return formatted_route_prefix
        


    