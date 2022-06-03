
from functools import singledispatch
from arq.exception.ipsum_exception import IpsumException
from arq.exception.exception_message import NOT_SUPPORTED_TYPES_EXCEPTION_MESSAGE

LEN = '__len__'

NOT_SUPPORTED_TYPES = [
    complex, range, set, frozenset,
    bytes, bytearray, memoryview
]

def is_none_or_empty(value, verify_iterable_values=True):
    _validate_type(value)

    if value is None:
        return True

    return _is_none_or_empty(value, verify_iterable_values=verify_iterable_values)

@singledispatch
def _is_none_or_empty(value, verify_iterable_values=True):
    
    if hasattr(value, LEN):
        return len(value) == 0

    return False

@_is_none_or_empty.register(bool)
def _(value, verify_iterable_values=True):
    return False

@_is_none_or_empty.register(int)
@_is_none_or_empty.register(float)
def _(value, verify_iterable_values=True):
    return value is None

@_is_none_or_empty.register(str)
def _(value, verify_iterable_values=True):
    return is_string_none_or_empty(value)

@_is_none_or_empty.register(list)
def _(value, verify_iterable_values=True):
    return is_list_none_or_empty(value, verify_iterable_values)

@_is_none_or_empty.register(tuple)
def _(value, verify_iterable_values=True):
    return is_tuple_none_or_empty(value, verify_iterable_values)

@_is_none_or_empty.register(dict)
def _(value, verify_iterable_values=True):
    return is_dict_none_or_empty(value, verify_iterable_values)

def is_string_none_or_empty(string: str):
    return len(string) == 0 or len(string.split()) == 0

def is_list_none_or_empty(lizt: list,  verify_iterable_values=True):
    if lizt == [] or len(lizt) == 0:
        return True

    if verify_iterable_values:
        return _is_iterable_values_none_or_empty(lizt)

    return False

def is_tuple_none_or_empty(tvple: tuple,  verify_iterable_values=True):
    if tvple == () or len(tvple) == 0:
        return True

    if verify_iterable_values:
        return _is_iterable_values_none_or_empty(tvple)

    return False

def is_dict_none_or_empty(dct: dict, verify_iterable_values=True):
    if dct == {} or len(dct) == 0:
        return True

    if verify_iterable_values:
        return _is_dict_values_none_or_empty(dct)

    return False

def _is_iterable_values_none_or_empty(iterable):
    for item in iterable:
        if not is_none_or_empty(item):
            return False
    
    return True

def _is_dict_values_none_or_empty(dct: dict):
    for key, value in dct.items():
        if not is_none_or_empty(value):
            return False

    return True

def _validate_type(value):
    tipe = type(value) 
    if tipe in NOT_SUPPORTED_TYPES:
        raise IpsumException(NOT_SUPPORTED_TYPES_EXCEPTION_MESSAGE.format(tipe))