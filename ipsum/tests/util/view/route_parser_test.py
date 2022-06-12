
from ipsum.util.view.route_parser import get_route_params, parse_route

# python3 -m pytest -p no:cacheprovider --capture=no ipsum/tests/util/view/route_parser_test.py

def test_route_parser():

    test_route = "parent/<parent_id>/child/<id>"

    parsed_route = parse_route(test_route, {"parent_id": 1, "id": 2})

    assert parsed_route == "parent/1/child/2"

def test_get_route_params():

    route = ' /some/path/here/now-parent-id/<parent_id>/now-id/action'
    expect = ['parent_id']
    assert get_route_params(route) == expect

    route = '/some/path/here/now-parent-id/<parent_id>/now-id'
    expect = ['parent_id']
    assert get_route_params(route) == expect

    route = '/some/path/here/now-parent-id/<parent_id>/now-id'
    expect = ['parent_id']
    assert get_route_params(route) == expect

    route = '/some/path/here/now-parent-id/<parent_id>/now-id/<id>'
    expect = ['parent_id', 'id']
    assert get_route_params(route) == expect

    route = '/some/path/here/now-parent-id/<parent_id>/now-id/<id>/one-more-id/<extra_id>'
    expect = ['parent_id', 'id', 'extra_id']
    assert get_route_params(route) == expect

    route = '/some/path/without/id'
    expect = []
    assert get_route_params(route) == expect

    route = ' /some/path/ with/spaces '
    expect = []
    assert get_route_params(route) == expect

    route = ' /some/path /<id>/ with/spaces '
    expect = ['id']
    assert get_route_params(route) == expect

    route = ' /some/path /<parent_id>/ with/spaces <id> '
    expect = ['parent_id', 'id']
    assert get_route_params(route) == expect

    route = 'some/path<parent_id>/child/<id>'
    expect = ['parent_id', 'id']
    assert get_route_params(route) == expect

