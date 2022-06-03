from ipsum.util import float_util

def test_is_string_int():

    assert float_util.is_string_float("0")
    assert float_util.is_string_float("0.1")
    assert float_util.is_string_float("0.")
    assert float_util.is_string_float(1)
    assert float_util.is_string_float(1.1)
    assert float_util.is_string_float(1.)

    assert not float_util.is_string_float("A")
    assert not float_util.is_string_float("A.")
    assert not float_util.is_string_float("A.A")
    assert not float_util.is_string_float(True)
    assert not float_util.is_string_float(False)
    