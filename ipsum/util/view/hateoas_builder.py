
import copy
from functools import singledispatchmethod
import json
from ipsum.util.view.route_parser import  parse_route
from ipsum.util.object_util import is_none_or_empty

class HATEOASBuilder:

    UTF8 = 'utf-8'

    _RULE_CACHE_ATTRIBUTE = '_rule_cache'

    def __init__(self, view, response_data, host_url, view_args) -> None:
        self.response_data = response_data
        self.view = view
        self.host_url = host_url
        self.view_args = view_args

    # TODO considerar tipo de dado 'response_data' ao fazer hateoas
    #
    # Rever
    # para dicionario fazer o hateoas de acordo com os ids:
    #   se nao tiver nenhum, trazer metodos que nao utilizam
    #   se tiver apenas id: trazers metodos que utilizam id 
    #   se tiver apenas parent_id: trazers metodos que utilizam parent_id 
    #   se tiver id e parent id: trazer metodos que usam ambos
    #
    # para registros que retornam lista:
    #   trazer links para cada registro
    # 
    # para 'paginate' trazer :
    #   para os items da listagem trazer da mesma forma que a lista
    #   
    #   para o objeto paginate:
    #       'last', 'next', 'previous', 'last', 'self'
    def build(self):

        data = self.get_response_data()

        return self._build_data(data)
        
    @singledispatchmethod
    def _build_data(self, data):
        return self.response_data

    @_build_data.register(list)
    def _(self, data):
        # TODO handle list
        # provisory
        return self.response_data

    @_build_data.register(dict)
    def _(self, item_data):
        # TODO HANDLE paginate
        data_with_links = self._build_item_data_links(item_data)

        return json.dumps(data_with_links).encode(self.UTF8)   


    def _build_item_data_links(self, item_data):
        item_data_with_links = copy.deepcopy(item_data)

        view_methods = self._get_view_methods()

        links = []
        for view_method in view_methods:
            params = self._build_params(item_data_with_links)

            method_links = self._build_method_links(view_method, params)

            links.extend(method_links)

        item_data_with_links['_links'] = links

        return item_data_with_links

    def get_response_data(self):
        if is_none_or_empty(self.response_data):
            return None

        if self._is_text_response():
            return json.loads(self.response_data)

        return self.response_data

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

            # TODO comparar os parametros do view_rule com os parametros de params (ou comparar apenas params)
            view_rule = self.view.build_rule(rule)

            parsed_route = parse_route(view_rule, params)

            parsed_route_without_initial_slash = parsed_route[1:]

            href = self.host_url + parsed_route_without_initial_slash

            method_link = {
                'name': view_method,
                'rel': rel,
                'href': href,
                'action': action
            }

            method_links.append(method_link)

        return method_links

    def _build_params(self, item_data):
        ID_KEY = 'id'

        args = self.view_args

        if is_none_or_empty(self.view_args):
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
        