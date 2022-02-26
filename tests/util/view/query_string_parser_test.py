from  api.utils.view.query_string_parser import QueryStringParser

def test_query_string_parser_parsing_decode():
    to_decode_query_string = {
        b'name': [b'encode'],
        b'encoded': [b'True', b'true', b'False', b'false'],
        'not_encoded': ['true'],
        b'encoded_key': ['value'],
        'decoded_key': [b'value encoded']
    }

    excpected_decoded_query_string = {
        'name': ['encode'],
        'encoded': ['True','True', 'False', 'False'],
        'not_encoded': ['true'],
        'encoded_key': ['value'],
        'decoded_key': ['value encoded']
    }

    decoded_query_string = QueryStringParser()._decode_parsed_query_string(to_decode_query_string)

    assert excpected_decoded_query_string == decoded_query_string

def test_query_string_parser_parsing_list_values():
    query_string_parser = QueryStringParser()

    query_string = 'name=joe&list=A&list=B'

    expected_parsed_query_string = {
        'name': 'joe',
        'list': ['A', 'B'],
    }

    parsed_query_string = query_string_parser.parse(query_string)

    assert expected_parsed_query_string == parsed_query_string


def test_query_string_parser_without_convert_string_to_boolean():
    query_string_parser = QueryStringParser(convert_string_to_boolean=False)

    query_string = 'name=joe&pinned=True&class=A&class=B'

    expected_parsed_query_string = {
        'name': 'joe',
        'pinned': 'True',
        'class': ['A', 'B'],
    }

    parsed_query_string = query_string_parser.parse(query_string)

    assert expected_parsed_query_string == parsed_query_string

def test_query_string_parser_converting_string_to_boolean():
    query_string_parser = QueryStringParser(convert_string_to_boolean=True)

    query_string = 'name=joe&pinned=True&class=A&class=B'

    expected_parsed_query_string = {
        'name': 'joe',
        'pinned': True,
        'class': ['A', 'B'],

    }

    parsed_query_string = query_string_parser.parse(query_string)

    assert expected_parsed_query_string == parsed_query_string

def test_query_string_parser_converting_string_to_boolean_ignoring_field_label():
    query_string_parser = QueryStringParser(convert_string_to_boolean=True, fields_to_boolean_to_ignore=['label'])

    query_string = 'name=joe&pinned=True&class=A&class=B&label=True'

    expected_parsed_query_string = {
        'name': 'joe',
        'pinned': True,
        'class': ['A', 'B'],
        'label': 'True'
    }

    parsed_query_string = query_string_parser.parse(query_string)

    assert expected_parsed_query_string == parsed_query_string

def test_query_string_parser_converting_string_list_to_boolean_list():
    query_string_parser = QueryStringParser(convert_string_to_boolean=True)

    query_string = 'name=joe&correct=True&correct=False&correct=true&correct=false'

    expected_parsed_query_string = {
        'name': 'joe',
        'correct': [True, False, True, False]
    }

    parsed_query_string = query_string_parser.parse(query_string)

    assert expected_parsed_query_string == parsed_query_string

def test_query_string_parser_not_converting_string_list_to_boolean_list_because_exists_non_boolean_values_in_it():
    query_string_parser = QueryStringParser(convert_string_to_boolean=True)

    query_string = 'name=joe&label=True&label=ok&label=fine&label=False'

    expected_parsed_query_string = {
        'name': 'joe',
        'label': ['True', 'ok', 'fine', 'False']
    }

    parsed_query_string = query_string_parser.parse(query_string)

    assert expected_parsed_query_string == parsed_query_string

def test_query_string_parser_converting_string_list_to_int_list():

    query_string_parser = QueryStringParser(convert_string_to_number=True)

    query_string = 'integer=100&codes=1&codes=2&codes=3'

    expected_parsed_query_string = {
        'integer': 100,
        'codes': [1, 2, 3]
    }

    parsed_query_string = query_string_parser.parse(query_string)

    assert expected_parsed_query_string == parsed_query_string

def test_query_string_parser_converting_string_list_to_int_list_ignoring_field_codes():

    query_string_parser = QueryStringParser(convert_string_to_number=True, fields_to_number_to_ignore=['codes'])

    query_string = 'integer=100&codes=1&codes=2&codes=3'

    expected_parsed_query_string = {
        'integer': 100,
        'codes': ['1', '2', '3']
    }

    parsed_query_string = query_string_parser.parse(query_string)

    assert expected_parsed_query_string == parsed_query_string

def test_query_string_parser_without_convert_string_list_to_int_list():

    query_string_parser = QueryStringParser(convert_string_to_number=False)

    query_string = 'integer=100&codes=1&codes=2&codes=3'

    expected_parsed_query_string = {
        'integer': '100',
        'codes': ['1', '2', '3']
    }

    parsed_query_string = query_string_parser.parse(query_string)

    assert expected_parsed_query_string == parsed_query_string

def test_query_string_parser_not_converting_string_list_to_int_list_because_exists_non_boolean_values_in_it():

    query_string_parser = QueryStringParser(convert_string_to_number=True)

    query_string = 'integer=100&codes=1&codes=A&codes=2&codes=3&codes=B'

    expected_parsed_query_string = {
        'integer': 100,
        'codes': ['1', 'A', '2', '3', 'B']
    }

    parsed_query_string = query_string_parser.parse(query_string)

    assert expected_parsed_query_string == parsed_query_string

def test_query_string_parser_converting_string_list_to_float_list():

    query_string_parser = QueryStringParser(convert_string_to_number=True, convert_number_only_to_float=True)

    query_string = 'float=100&codes=1&codes=2&codes=3'

    expected_parsed_query_string = {
        'float': 100,
        'codes': [1, 2, 3]
    }

    parsed_query_string = query_string_parser.parse(query_string)

    assert expected_parsed_query_string == parsed_query_string

def test_query_string_parser_converting_string_list_to_float_list_ignoring_field_codes():

    query_string_parser = QueryStringParser(convert_string_to_number=True, fields_to_number_to_ignore=['codes'], convert_number_only_to_float=True)

    query_string = 'float=100&codes=1&codes=2&codes=3'

    expected_parsed_query_string = {
        'float': 100,
        'codes': ['1', '2', '3']
    }

    parsed_query_string = query_string_parser.parse(query_string)

    assert expected_parsed_query_string == parsed_query_string

def test_query_string_parser_without_convert_string_list_to_float_list():

    query_string_parser = QueryStringParser(convert_string_to_number=False, convert_number_only_to_float=True)

    query_string = 'float=100&codes=1&codes=2&codes=3'

    expected_parsed_query_string = {
        'float': '100',
        'codes': ['1', '2', '3']
    }

    parsed_query_string = query_string_parser.parse(query_string)

    assert expected_parsed_query_string == parsed_query_string

def test_query_string_parser_not_converting_string_list_to_float_list_because_exists_non_boolean_values_in_it():

    query_string_parser = QueryStringParser(convert_string_to_number=True, convert_number_only_to_float=True)

    query_string = 'float=100&codes=1&codes=A&codes=2&codes=3&codes=B'

    expected_parsed_query_string = {
        'float': 100,
        'codes': ['1', 'A', '2', '3', 'B']
    }

    parsed_query_string = query_string_parser.parse(query_string)

    assert expected_parsed_query_string == parsed_query_string


def test_query_string_parser_converting_string_list_to_number_list_considering_floats_and_ints():

    query_string_parser = QueryStringParser(convert_string_to_number=True)

    query_string = 'sum=100&codes=1&codes=2&codes=3&vals=1.0&vals=2.0&vals=3.0&mix=1&mix=2.0&mix=3&mix=4.0'

    expected_parsed_query_string = {
        'sum': 100,
        'codes': [1, 2, 3],
        'vals': [1.0, 2.0, 3.0],
        'mix': [1, 2.0, 3, 4.0]
    }

    parsed_query_string = query_string_parser.parse(query_string)

    assert expected_parsed_query_string == parsed_query_string