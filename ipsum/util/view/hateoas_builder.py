
import copy
from functools import singledispatchmethod
import json
from ipsum.util.data.pagination import Pagination
from ipsum.util.list_util import list_equals
from ipsum.util.view.route_parser import  get_route_params, parse_route
from ipsum.util.object_util import is_none_or_empty
from ipsum.view import ipsum_view

# TODO build 'self' to item_data
# TODO add 'insert' in pagination methods
class HATEOASBuilder:

    UTF8 = 'utf-8'

    _RULE_CACHE_ATTRIBUTE = '_rule_cache'

    HATEOAS_LINKS = '_links'

    def __init__(self, view, response_data, host_url, view_args, request_name, query_string) -> None:
        self.response_data = response_data
        self.view = view
        self.host_url = host_url
        self.view_args = view_args
        self.request_name = request_name
        self.query_string = query_string

        if type(query_string) is bytes:
            self.query_string = query_string.decode(self.UTF8)


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

        item_data_with_link[self.HATEOAS_LINKS] = self._build_paginate_links(item_data)

        return item_data_with_link 

    def _build_item_links(self, item_data):
        items_with_links = self._build_data(item_data[Pagination.ITEMS])

        items_with_links = json.loads(items_with_links)

        item_data_with_link = copy.deepcopy(item_data)

        item_data_with_link[Pagination.ITEMS] = items_with_links
        return item_data_with_link 


    def _build_item_data_links(self, item_data):
        item_data_with_links = copy.deepcopy(item_data)

        view_methods = self._get_view_methods()

        links = []
        for view_method in view_methods:
            params = self._build_params(item_data_with_links)

            method_links = self._build_method_links(view_method, params)

            links.extend(method_links)

        parent_link = self._build_parent_link()
        if not is_none_or_empty(parent_link):
            links.append(parent_link)

        child_links = self._build_child_links(item_data)
        if not is_none_or_empty(child_links):
            links.extend(child_links)

        item_data_with_links[self.HATEOAS_LINKS] = links

        return item_data_with_links

    def _build_paginate_links(self, item_data):

        rel = self.view.get_route_base()
        
        actions = self._get_actions(self.request_name)

        rules = self._get_rules(self.request_name)

        request_links = self._build_request_links(actions, rules)
            
        paginate_query_params = self._get_paginate_query_params(item_data)

        paginate_links = []
        for name, params in paginate_query_params.items():

            if not params is None:

                for request_link in request_links:
                    rel_query_string = self._build_related_query_string(paginate_query_params, params)

                    href = f'{request_link["href"]}?{rel_query_string}'

                    paginate_link = {
                        'name': name,
                        'rel': rel,
                        'href': href,
                        'action': request_link['action']
                    }

                    paginate_links.append(paginate_link)

        return paginate_links

    def _build_related_query_string(self, paginate_query_params, params):
        query_string = self.query_string
                    
        self_rel = paginate_query_params[Pagination.SELF]

        self_rel_offset = self_rel[Pagination.OFFSET]
        self_rel_offset_query = f'{ipsum_view.QUERY_OFFSET}={self_rel_offset}'

        rel_offset_query = f'{ipsum_view.QUERY_OFFSET}={params[Pagination.OFFSET]}'
        rel_query_string = query_string

        if ipsum_view.QUERY_OFFSET in query_string:
            rel_query_string = rel_query_string.replace(self_rel_offset_query, rel_offset_query)

        else:
            if not is_none_or_empty(rel_query_string):
                rel_query_string += '&'

            rel_query_string += rel_offset_query
        return rel_query_string

    def _build_request_links(self, actions, rules):
        request_links = []
        for i in range(len(rules)):
            href = self._build_href(rules[i], validate_params=False)

            action = actions[i]
            request_link = {
                'href': href,
                'action': action, 
            }

            request_links.append(request_link)
        return request_links

    def _get_paginate_query_params(self, item_data):
        return Pagination([]).related_info(item_data[Pagination.INFO])


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
        return ipsum_view.IpsumView.PAGINATE_REQUEST == self.request_name

    def _is_paginate(self, item_data):
        item_keys = list(item_data.keys())

        for key in Pagination.KEYS:
            if key not in item_keys:
                return False

        return True

    def _is_text_response(self):
        return type(self.response_data) is bytes or type(self.response_data) is str

    def _build_method_links(self, view_method, params, rel=None):
        _rel = rel
        
        if _rel is None:
            _rel = self.view.get_route_base()
            
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
                    'rel': _rel,
                    'href': href,
                    'action': action
                }

                method_links.append(method_link)

        return method_links

    def _build_parent_link(self):
        
        parent_params = copy.deepcopy(self.view_args)
        if 'id' in parent_params:
            parent_params.pop('id')

        if not is_none_or_empty(parent_params):

            parent_route = self.host_url + self.view.route_prefix
            href = parse_route(parent_route, parent_params)
            href = href[:-1]

            parent_link = {
                'name': ipsum_view.FIND_BY_ID,
                'rel': 'parent',
                'href': href,
                'action': [ipsum_view.GET]
            }

            return parent_link

        return None

    def _build_child_links(self, item_data):
        if not is_none_or_empty(self.view.child_collections):
            child_links = []

            for child in self.view.child_collections:
                child_view = child.view
                child_parent_field = child.id_field

                child_view_args = {child_parent_field: item_data['id']}
                child_hateoas_builder = HATEOASBuilder(
                    view=child_view, response_data=[], host_url=self.host_url,
                    view_args=child_view_args, request_name='', query_string=''
                )

                child_params = child_hateoas_builder._build_params(use_id=False)

                insert_links = child_hateoas_builder._build_method_links(child_view.INSERT_REQUEST, child_params)                
                child_links.extend(insert_links)

                paginate_links = child_hateoas_builder._build_method_links(child_view.PAGINATE_REQUEST, child_params)
                child_links.extend(paginate_links)

            return child_links

        return None

    def _build_params(self, item_data=None, use_id=True):
        ID_KEY = 'id'

        args = self.view_args

        if is_none_or_empty(self.view_args) and not self._is_paginate_request_name():
            args = {'id': None}

        elif ID_KEY not in args and use_id:
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
        