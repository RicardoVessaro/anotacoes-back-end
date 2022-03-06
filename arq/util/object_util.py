
from arq.exception.arq_exception import ArqException


NOT_SUPPORTED_TYPES_EXCEPTION_MESSAGE = "The type '{0}' is not supported."

NOT_SUPPORTED_TYPES = [
    int, float, complex, range, set, frozenset,
    bytes, bytearray, memoryview
]

def is_none_or_empty(value, verify_iterable_values=True):
    _validate_type(value)

    if value is None:
        return True

    elif value is bool:
        return False
    
    elif type(value) is str:
        return is_string_none_or_empty(value)

    elif type(value) is list:
        return is_list_none_or_empty(value, verify_iterable_values)

    elif type(value) is tuple:
        return is_tuple_none_or_empty(value, verify_iterable_values)

    elif type(value) is dict:
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
        raise ArqException(NOT_SUPPORTED_TYPES_EXCEPTION_MESSAGE.format(tipe))