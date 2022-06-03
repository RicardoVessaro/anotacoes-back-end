from ipsum.util import int_util

def test_is_string_int():

    assert int_util.is_string_int("0")
    assert int_util.is_string_int(1)

    assert not int_util.is_string_int("A")
    assert not int_util.is_string_int(False)
    assert not int_util.is_string_int(True)
    
