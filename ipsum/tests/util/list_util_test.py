
from ipsum.util.list_util import list_equals


def test_list_equals():

    left_list = ['a', 'b']
    right_list = ['a', 'b']
    assert list_equals(left_list, right_list)

    left_list = ['a', 'b']
    right_list = ['b', 'a']
    assert not list_equals(left_list, right_list)

    left_list = ['a', 'b']
    right_list = ['b', 'a']
    assert list_equals(left_list, right_list, validate_order=False)

    left_list = ['a', 'b', 'c']
    right_list = ['b', 'a']
    assert not list_equals(left_list, right_list, validate_order=False)

    left_list = ['b', 'a']
    right_list = ['a', 'b', 'c']
    assert not list_equals(left_list, right_list, validate_order=False)