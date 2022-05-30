
def parse_route(route:str, params:dict):
    parsed_route = route
    for param, value in params.items():
        parsed_route = parsed_route.replace(f'<{param}>', str(value))

    return parsed_route
