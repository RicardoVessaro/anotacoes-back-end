
import copy
from functools import singledispatchmethod
import json
from ipsum.util.list_util import list_equals
from ipsum.util.view.route_parser import  get_route_params, parse_route
from ipsum.util.object_util import is_none_or_empty

class HATEOASBuilder:

    UTF8 = 'utf-8'

    _RULE_CACHE_ATTRIBUTE = '_rule_cache'

    # TODO Criar 'pagination_util'
    # TODO referenciar pagination_util
    _PAGINATE_KEY_ITEMS = 'items'

    _HATEOAS_LINKS = '_links'

    # TODO referenciar IpsumView e DetailCRUDView
    _PAGINATE_REQUEST_NAME = 'find'

    # TODO referenciar pagination_util
    _PAGINATE_KEYS = [
        'has_next', 'has_prev', 'has_result', _PAGINATE_KEY_ITEMS, 'limit', 'page', 
        'pages', 'total'
    ]

    def __init__(self, view, response_data, host_url, view_args, request_name) -> None:
        self.response_data = response_data
        self.view = view
        self.host_url = host_url
        self.view_args = view_args
        self.request_name = request_name

    def build(self):

        data = self.get_response_data()

        return self._build_data(data)
        
    @singledispatchmethod
    def _build_data(self, data):
        return self.response_data

    @_build_data.register(list)
    def _(self, data):
        data_with_links = []
        for item_data in data:
            item_data_with_links = self._build_item_data_links(item_data)

            data_with_links.append(item_data_with_links)

        return json.dumps(data_with_links).encode(self.UTF8)   

    @_build_data.register(dict)
    def _(self, item_data):
        if self._is_paginate(item_data):
            item_data_with_link = self._handle_paginate_response(item_data)

            return json.dumps(item_data_with_link).encode(self.UTF8)

        data_with_links = self._build_item_data_links(item_data)

        return json.dumps(data_with_links).encode(self.UTF8) 

    def _handle_paginate_response(self, item_data):
        item_data_with_link = self._build_item_links(item_data)

        item_data_with_link[self._HATEOAS_LINKS] = self._build_paginate_links()

        return item_data_with_link 

    def _build_item_links(self, item_data):
        items_with_links = self._build_data(item_data[self._PAGINATE_KEY_ITEMS])

        items_with_links = json.loads(items_with_links)

        item_data_with_link = copy.deepcopy(item_data)

        item_data_with_link[self._PAGINATE_KEY_ITEMS] = items_with_links
        return item_data_with_link 


    def _build_item_data_links(self, item_data):
        item_data_with_links = copy.deepcopy(item_data)

        view_methods = self._get_view_methods()

        links = []
        for view_method in view_methods:
            params = self._build_params(item_data_with_links)

            method_links = self._build_method_links(view_method, params)

            links.extend(method_links)

        item_data_with_links[self._HATEOAS_LINKS] = links

        return item_data_with_links

    def _build_paginate_links(self):

        rel = self.view.get_route_base()
        
        actions = self._get_actions(self.request_name)

        rules = self._get_rules(self.request_name)

        request_links = []
        for i in range(len(rules)):
            
            href = self._build_href(rules[i], validate_params=False)

            action = actions[i]
            request_link = {
                'href': href,
                'action': action, 
            }

            request_links.append(request_link)
            
        # TODO self, next, previous, first, last (ver pagination_util)
        # TODO so falta fazer a busca pelo paginate_query_params no 'pagination_util'
        paginate_query_params = ['self', 'next', 'previous', 'first', 'last']
        paginate_links = []
        for query_param in paginate_query_params:

            for request_link in request_links:
                name = 'query_param[0]' + query_param

                paginate_link = {
                    'name': name,
                    'rel': rel,
                    'href': request_link['href'],
                    'action': request_link['action']
                }

                paginate_links.append(paginate_link)

        return paginate_links

    def _build_href(self, rule, params=None, validate_params=True):
        view_rule = self.view.build_rule(rule)
            
        _params = params
        if _params is None:
            _params = self._build_params()

        parsed_route = parse_route(view_rule, _params)
        parsed_route_without_initial_slash = parsed_route[1:]

        href = self.host_url + parsed_route_without_initial_slash

        if validate_params:
            if self._params_equals_params_in_view_rule(params, view_rule):
                return href
            
            return None

        return href


    def get_response_data(self):
        if is_none_or_empty(self.response_data):
            return None

        if self._is_text_response():
            return json.loads(self.response_data)

        return self.response_data

    def _is_paginate_request_name(self):
        return self._PAGINATE_REQUEST_NAME == self.request_name

    def _is_paginate(self, item_data):
        item_keys = list(item_data.keys())

        for key in self._PAGINATE_KEYS:
            if key not in item_keys:
                return False

        return True

    def _is_text_response(self):
        return type(self.response_data) is bytes or type(self.response_data) is str

    def _build_method_links(self, view_method, params):
        rel = self.view.get_route_base()
            
        actions = self._get_actions(view_method)

        rules = self._get_rules(view_method)

        method_links = []
        for i in range(len(rules)):
            rule = rules[i]
            action = actions[i]

            href = self._build_href(rule, params=params)

            if not href is None:
                method_link = {
                    'name': view_method,
                    'rel': rel,
                    'href': href,
                    'action': action
                }

                method_links.append(method_link)

        return method_links

    def _build_params(self, item_data=None):
        ID_KEY = 'id'

        args = self.view_args

        if is_none_or_empty(self.view_args) and not self._is_paginate_request_name():
            args = {'id': None}

        elif ID_KEY not in args:
            args[ID_KEY] = None

        if is_none_or_empty(item_data):
            return args

        params = {}
        for key in args:
            if key in item_data:
                params[key] = item_data[key]

        return params

    def _get_view_methods(self):
        _dir = dir(self.view)

        view_methods = []

        for d in _dir:
            d_attr = self._get_method(d)

            if hasattr(d_attr, self._RULE_CACHE_ATTRIBUTE):
                view_methods.append(d)

        return view_methods

    def _params_equals_params_in_view_rule(self, params, view_rule):
        view_rule_params = get_route_params(view_rule)

        params_keys = list(params.keys())

        return list_equals(view_rule_params, params_keys, validate_order=False)

    def _get_rules(self, view_method_name):
        RULE_CACHE_RULE_TUPLE_COOLUMN = 0

        rules = []

        rule_cache = self._get_method_rule_cache(view_method_name)

        for rule_tuple in rule_cache:
            rules.append(rule_tuple[RULE_CACHE_RULE_TUPLE_COOLUMN])

        return rules

    def _get_actions(self, view_method_name):
        RULE_CACHE_ACTION_TUPLE_COOLUMN = 1
        METHODS_KEY = 'methods'

        actions = []

        rule_cache = self._get_method_rule_cache(view_method_name)

        for rule_tuple in rule_cache:
            actions.append(rule_tuple[RULE_CACHE_ACTION_TUPLE_COOLUMN][METHODS_KEY])

        return actions

    def _get_method_rule_cache(self, view_method_name):
        view_method = self._get_method(view_method_name)

        rule_cache = view_method._rule_cache[view_method_name]
        return rule_cache

    def _get_method(self, method_name):
        return getattr(self.view, method_name)
        