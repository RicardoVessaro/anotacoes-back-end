
import re

from ipsum.util.object_util import is_none_or_empty


def parse_route(route:str, params:dict):
    parsed_route = route
    for param, value in params.items():
        parsed_route = parsed_route.replace(f'<{param}>', str(value))

    return parsed_route


def get_route_params(route:str):
    pattern = '[<>]'

    paths = re.split(pattern, route)

    params = []

    for string in paths:
        
        if not is_none_or_empty(string) and not string.startswith('/') and not string.endswith('/'):
            params.append(string)

    return params
