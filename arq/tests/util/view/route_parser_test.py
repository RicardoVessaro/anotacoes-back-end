
from arq.util.view.route_parser import parse_route

def test_route_parser():

    test_route = "parent/<parent_id>/child/<id>"

    parsed_route = parse_route(test_route, {"parent_id": 1, "id": 2})

    assert parsed_route == "parent/1/child/2"

