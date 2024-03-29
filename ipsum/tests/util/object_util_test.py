from pytest import raises
from collections import namedtuple
from array import array
from ipsum.exception.ipsum_exception import IpsumException
from ipsum.util.object_util import is_iterable, is_none_or_empty, NOT_SUPPORTED_TYPES, NOT_SUPPORTED_TYPES_EXCEPTION_MESSAGE

def test_none_value():
    assert is_none_or_empty(None)

def test_bytes():

    assert is_none_or_empty(b'')
    assert is_none_or_empty(b'    ')
    assert not is_none_or_empty(b'None')
    assert not is_none_or_empty(b'bytes')

def test_default_value():

    def test_namedtuple():
        test = namedtuple('Test', 'name')
        t1 = test(name='t1')

        assert not is_none_or_empty(t1)

    test_namedtuple()

    def test_array():

        ints = array('i')

        assert is_none_or_empty(ints)

        ints.append(1)
        ints.append(6)

        assert not is_none_or_empty(ints)

    test_array()
    

def test_boolean_value():
    assert not is_none_or_empty(True)
    assert not is_none_or_empty(False)

def test_int_value():
    assert not is_none_or_empty(1)

def test_float_value():
    assert not is_none_or_empty(1.0)

def test_string_value():
    assert is_none_or_empty("")
    assert is_none_or_empty("    ")
    assert not is_none_or_empty("None")

def test_list_value():
    assert is_none_or_empty([])
    assert is_none_or_empty([[], []])
    assert is_none_or_empty([
        [], None, "", ["", None],  (),
    ])

    assert is_none_or_empty([], verify_iterable_values=False)
    assert not is_none_or_empty([
        [], None, "", ["", None],  (),
    ], verify_iterable_values=False)
    assert not is_none_or_empty([[], []], verify_iterable_values=False)
    
def test_tuple_value():
    assert is_none_or_empty(())
    assert is_none_or_empty(((), ()))
    assert is_none_or_empty((
        [], None, "", ("", None),  (),
    ))

    assert is_none_or_empty((), verify_iterable_values=False)
    assert not is_none_or_empty((
        [], None, "", ("", None),  (),
    ), verify_iterable_values=False)
    assert not is_none_or_empty(((), ()), verify_iterable_values=False)
NOT_SUPPORTED_TYPES_EXCEPTION_MESSAGE
def test_dict_value():
    assert is_none_or_empty({})
    assert is_none_or_empty({
        "a": None, 
        "b": [], 
        "c": (),
        "d": "",
        "e": [[], ()],
        "f": ((), []),
        "g": {},
        "h": {
           "1" : None,
           "2": {},
           "3": "",
           "4": ((), []),
           "5": [[], ()]
        }
    })

    assert is_none_or_empty({}, verify_iterable_values=False)
    assert not is_none_or_empty({
        "a": None, 
        "b": [], 
        "c": (),
        "d": "",
        "e": [[], ()],
        "f": ((), []),
        "g": {},
        "h": {
           "1" : None,
           "2": {},
           "3": "",
           "4": ((), []),
           "5": [[], ()]
        }
    }, verify_iterable_values=False)

def test_boolean_value():
    assert is_none_or_empty(None)
    assert not is_none_or_empty(False)
    assert not is_none_or_empty(True)


def test_not_supported_type():
    for not_supported_type in NOT_SUPPORTED_TYPES:

        if not_supported_type is range:
            type_call = not_supported_type(1)
        
        elif not_supported_type is memoryview:
            type_call = not_supported_type(b'm')
            
        else :   
            type_call = not_supported_type()

        str_type = str(type(type_call))

        with raises(IpsumException, match=NOT_SUPPORTED_TYPES_EXCEPTION_MESSAGE.format(str_type)):
            is_none_or_empty(type_call)

def test_is_iterable():

    assert True == is_iterable([])
    assert True == is_iterable("string")
    assert True == is_iterable({})
    assert False == is_iterable(1)
    assert False == is_iterable(1.0)
