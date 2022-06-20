from  ipsum.util.view.query_string_parser import QueryStringParser

def test_query_string_parser_with_separator_and_space_filters():


    def _test_query_string_parser_parsing_filter_queries():
        query_string = 'title[or:eq]=Link 10|Link 11'

        expected_query_string = {
            'title[or:eq]': ['Link 10', 'Link 11']
        }

        parsed_query_string = QueryStringParser().parse_string(query_string)

        assert expected_query_string == parsed_query_string

    _test_query_string_parser_parsing_filter_queries()



    def _complex_query_string(): 
        query_string = '_op=and&code[or:eq]=1&code[or:eq]=2&priority[lte]=1&tags[in]=A&boolean=true&_sort=-code&_sort=date&_fields=code&_fields=title'

        expected_query_string = {
            '_op': 'and',
            'code[or:eq]': [1, 2],
            'priority[lte]': 1,
            'tags[in]': ['A'],
            'boolean': True,
            '_sort': ['-code', 'date'],
            '_fields': ['code', 'title']
        }

        parsed_query_string = QueryStringParser().parse_string(query_string)

        assert expected_query_string == parsed_query_string

    _complex_query_string()

    def _complex_query_string_using_separator(): 
        query_string = '_op=and&code[or:eq]=1|2&priority[lte]=1&tags[in]=A&boolean=true&_sort=-code|date&_fields=code|title'

        expected_query_string = {
            '_op': 'and',
            'code[or:eq]': [1, 2],
            'priority[lte]': 1,
            'tags[in]': ['A'],
            'boolean': True,
            '_sort': ['-code', 'date'],
            '_fields': ['code', 'title']
        }

        parsed_query_string = QueryStringParser().parse_string(query_string)

        assert expected_query_string == parsed_query_string

    _complex_query_string_using_separator()

    def _complex_query_string_using_ipsum_params(): 
        query_string = '_op=and&code[or:eq]=1|2&priority[lte]=1&tags[in]=A|B&boolean=true&_sort=-code|date&_fields=code|title&_offset=5&_limit=10'

        expected_query_string = {
            '_op': 'and',
            'code[or:eq]': [1, 2],
            'priority[lte]': 1,
            'tags[in]': ['A', 'B'],
            'boolean': True,
            '_sort': ['-code', 'date'],
            '_fields': ['code', 'title'],
            '_offset': 5,
            '_limit': 10
        }

        parsed_query_string = QueryStringParser().parse_string(query_string)

        assert expected_query_string == parsed_query_string

    _complex_query_string_using_ipsum_params()

def test_list_operators_with_single_list_values():

    def _in_operator(): 
        query_string = 'tags[in]=A'

        expected_query_string = {'tags[in]': ['A']}

        parsed_query_string = QueryStringParser().parse_string(query_string)

        assert expected_query_string == parsed_query_string

    _in_operator()

    def _nin_operator(): 
        query_string = 'tags[nin]=A'

        expected_query_string = {'tags[nin]': ['A']}

        parsed_query_string = QueryStringParser().parse_string(query_string)

        assert expected_query_string == parsed_query_string

    _nin_operator()

    def _aeq_operator(): 
        query_string = 'tags[aeq]=A'

        expected_query_string = {'tags[aeq]': ['A']}

        parsed_query_string = QueryStringParser().parse_string(query_string)

        assert expected_query_string == parsed_query_string

    _aeq_operator()

    
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

    parsed_query_string = query_string_parser.parse_string(query_string)

    assert expected_parsed_query_string == parsed_query_string


def test_query_string_parser_without_convert_string_to_boolean():
    query_string_parser = QueryStringParser(convert_string_to_boolean=False)

    query_string = 'name=joe&pinned=True&class=A&class=B'

    expected_parsed_query_string = {
        'name': 'joe',
        'pinned': 'True',
        'class': ['A', 'B'],
    }

    parsed_query_string = query_string_parser.parse_string(query_string)

    assert expected_parsed_query_string == parsed_query_string

def test_query_string_parser_converting_string_to_boolean():
    query_string_parser = QueryStringParser(convert_string_to_boolean=True)

    query_string = 'name=joe&pinned=True&class=A&class=B'

    expected_parsed_query_string = {
        'name': 'joe',
        'pinned': True,
        'class': ['A', 'B'],

    }

    parsed_query_string = query_string_parser.parse_string(query_string)

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

    parsed_query_string = query_string_parser.parse_string(query_string)

    assert expected_parsed_query_string == parsed_query_string

def test_query_string_parser_converting_string_list_to_boolean_list():
    query_string_parser = QueryStringParser(convert_string_to_boolean=True)

    query_string = 'name=joe&correct=True&correct=False&correct=true&correct=false'

    expected_parsed_query_string = {
        'name': 'joe',
        'correct': [True, False, True, False]
    }

    parsed_query_string = query_string_parser.parse_string(query_string)

    assert expected_parsed_query_string == parsed_query_string

def test_query_string_parser_not_converting_string_list_to_boolean_list_because_exists_non_boolean_values_in_it():
    query_string_parser = QueryStringParser(convert_string_to_boolean=True)

    query_string = 'name=joe&label=True&label=ok&label=fine&label=False'

    expected_parsed_query_string = {
        'name': 'joe',
        'label': ['True', 'ok', 'fine', 'False']
    }

    parsed_query_string = query_string_parser.parse_string(query_string)

    assert expected_parsed_query_string == parsed_query_string

def test_query_string_parser_converting_string_list_to_int_list():

    query_string_parser = QueryStringParser(convert_string_to_number=True)

    query_string = 'integer=100&codes=1&codes=2&codes=3'

    expected_parsed_query_string = {
        'integer': 100,
        'codes': [1, 2, 3]
    }

    parsed_query_string = query_string_parser.parse_string(query_string)

    assert expected_parsed_query_string == parsed_query_string

def test_query_string_parser_converting_string_list_to_int_list_ignoring_field_codes():

    query_string_parser = QueryStringParser(convert_string_to_number=True, fields_to_number_to_ignore=['codes'])

    query_string = 'integer=100&codes=1&codes=2&codes=3'

    expected_parsed_query_string = {
        'integer': 100,
        'codes': ['1', '2', '3']
    }

    parsed_query_string = query_string_parser.parse_string(query_string)

    assert expected_parsed_query_string == parsed_query_string

def test_query_string_parser_without_convert_string_list_to_int_list():

    query_string_parser = QueryStringParser(convert_string_to_number=False)

    query_string = 'integer=100&codes=1&codes=2&codes=3'

    expected_parsed_query_string = {
        'integer': '100',
        'codes': ['1', '2', '3']
    }

    parsed_query_string = query_string_parser.parse_string(query_string)

    assert expected_parsed_query_string == parsed_query_string

def test_query_string_parser_not_converting_string_list_to_int_list_because_exists_non_boolean_values_in_it():

    query_string_parser = QueryStringParser(convert_string_to_number=True)

    query_string = 'integer=100&codes=1&codes=A&codes=2&codes=3&codes=B'

    expected_parsed_query_string = {
        'integer': 100,
        'codes': ['1', 'A', '2', '3', 'B']
    }

    parsed_query_string = query_string_parser.parse_string(query_string)

    assert expected_parsed_query_string == parsed_query_string

def test_query_string_parser_converting_string_list_to_float_list():

    query_string_parser = QueryStringParser(convert_string_to_number=True, convert_number_only_to_float=True)

    query_string = 'float=100&codes=1&codes=2&codes=3'

    expected_parsed_query_string = {
        'float': 100.0,
        'codes': [1, 2, 3]
    }

    parsed_query_string = query_string_parser.parse_string(query_string)

    assert expected_parsed_query_string == parsed_query_string

def test_query_string_parser_converting_string_list_to_float_list_ignoring_field_codes():

    query_string_parser = QueryStringParser(convert_string_to_number=True, fields_to_number_to_ignore=['codes'], convert_number_only_to_float=True)

    query_string = 'float=100&codes=1&codes=2&codes=3'

    expected_parsed_query_string = {
        'float': 100.0,
        'codes': ['1', '2', '3']
    }

    parsed_query_string = query_string_parser.parse_string(query_string)

    assert expected_parsed_query_string == parsed_query_string

def test_query_string_parser_without_convert_string_list_to_float_list():

    query_string_parser = QueryStringParser(convert_string_to_number=False, convert_number_only_to_float=True)

    query_string = 'float=100&codes=1&codes=2&codes=3'

    expected_parsed_query_string = {
        'float': '100',
        'codes': ['1', '2', '3']
    }

    parsed_query_string = query_string_parser.parse_string(query_string)

    assert expected_parsed_query_string == parsed_query_string

def test_query_string_parser_not_converting_string_list_to_float_list_because_exists_non_boolean_values_in_it():

    query_string_parser = QueryStringParser(convert_string_to_number=True, convert_number_only_to_float=True)

    query_string = 'float=100&codes=1&codes=A&codes=2&codes=3&codes=B'

    expected_parsed_query_string = {
        'float': 100,
        'codes': ['1', 'A', '2', '3', 'B']
    }

    parsed_query_string = query_string_parser.parse_string(query_string)

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

    parsed_query_string = query_string_parser.parse_string(query_string)

    assert expected_parsed_query_string == parsed_query_string

def test_query_string_parser_transform_dict_to_query_dict():

    query_string_parser = QueryStringParser()

    query_dict = {
        'bool': 'True',
        'numbers': [1, 2, 3],
        'text': 'lorem',
    }

    transformed_query_string = query_string_parser._transform_to_query(query_dict)

    expected_query_dict = {
        'bool': ['True'],
        'numbers': [1, 2, 3],
        'text': ['lorem'],
    }

    assert expected_query_dict == transformed_query_string

def test_query_dict_parser_parsing_list_values():
    query_string_parser = QueryStringParser()

    query_dict = {
        'name': 'joe',
        'list': ['A', 'B']
    }

    expected_parsed_query_dict = {
        'name': 'joe',
        'list': ['A', 'B'],
    }

    parsed_query_dict = query_string_parser.parse_dict(query_dict)

    assert expected_parsed_query_dict == parsed_query_dict


def test_query_dict_parser_without_convert_string_to_boolean():
    query_string_parser = QueryStringParser(convert_string_to_boolean=False)

    query_dict = {
        'name': 'joe',
        'pinned': 'True',
        'class': ['A', 'B']
    }

    expected_parsed_query_dict = {
        'name': 'joe',
        'pinned': 'True',
        'class': ['A', 'B'],
    }

    parsed_query_dict = query_string_parser.parse_dict(query_dict)

    assert expected_parsed_query_dict == parsed_query_dict

def test_query_dict_parser_converting_string_to_boolean():
    query_string_parser = QueryStringParser(convert_string_to_boolean=True)

    query_dict = {
        'name': 'joe',
        'pinned': True,
        'class': ['A', 'B']
    }

    expected_parsed_query_dict = {
        'name': 'joe',
        'pinned': True,
        'class': ['A', 'B'],

    }

    parsed_query_dict = query_string_parser.parse_dict(query_dict)

    assert expected_parsed_query_dict == parsed_query_dict

def test_query_dict_parser_converting_string_to_boolean_ignoring_field_label():
    query_string_parser = QueryStringParser(convert_string_to_boolean=True, fields_to_boolean_to_ignore=['label'])

    query_dict = {
        'name': 'joe',
        'pinned': True,
        'class': ['A', 'B'],
        'label': 'True'
    }

    expected_parsed_query_dict = {
        'name': 'joe',
        'pinned': True,
        'class': ['A', 'B'],
        'label': 'True'
    }

    parsed_query_dict = query_string_parser.parse_dict(query_dict)

    assert expected_parsed_query_dict == parsed_query_dict

def test_query_dict_parser_converting_string_list_to_boolean_list():
    query_string_parser = QueryStringParser(convert_string_to_boolean=True)

    query_dict = {
        'name': 'joe',
        'correct': [True, False, True, False],
    }

    expected_parsed_query_dict = {
        'name': 'joe',
        'correct': [True, False, True, False]
    }

    parsed_query_dict = query_string_parser.parse_dict(query_dict)

    assert expected_parsed_query_dict == parsed_query_dict

def test_query_dict_parser_not_converting_string_list_to_boolean_list_because_exists_non_boolean_values_in_it():
    query_string_parser = QueryStringParser(convert_string_to_boolean=True)

    query_dict = {
        'name': 'joe',
        'label': ['True', 'ok', 'fine', 'False']
    }

    expected_parsed_query_dict = {
        'name': 'joe',
        'label': ['True', 'ok', 'fine', 'False']
    }

    parsed_query_dict = query_string_parser.parse_dict(query_dict)

    assert expected_parsed_query_dict == parsed_query_dict

def test_query_dict_parser_converting_string_list_to_int_list():

    query_string_parser = QueryStringParser(convert_string_to_number=True)

    query_dict = {
        'integer': 100,
        'codes': [1, 2, 3]
    }

    expected_parsed_query_dict = {
        'integer': 100,
        'codes': [1, 2, 3]
    }

    parsed_query_dict = query_string_parser.parse_dict(query_dict)

    assert expected_parsed_query_dict == parsed_query_dict

def test_query_dict_parser_converting_string_list_to_int_list_ignoring_field_codes():

    query_string_parser = QueryStringParser(convert_string_to_number=True, fields_to_number_to_ignore=['codes'])

    query_dict = {
        'integer': 100,
        'codes': ['1', '2', '3']
    }

    expected_parsed_query_dict = {
        'integer': 100,
        'codes': ['1', '2', '3']
    }

    parsed_query_dict = query_string_parser.parse_dict(query_dict)

    assert expected_parsed_query_dict == parsed_query_dict

def test_query_dict_parser_without_convert_string_list_to_int_list():

    query_string_parser = QueryStringParser(convert_string_to_number=False)

    query_dict = {
        'integer': '100',
        'codes': ['1', '2', '3']
    }

    expected_parsed_query_dict = {
        'integer': '100',
        'codes': ['1', '2', '3']
    }

    parsed_query_dict = query_string_parser.parse_dict(query_dict)

    assert expected_parsed_query_dict == parsed_query_dict

def test_query_dict_parser_not_converting_string_list_to_int_list_because_exists_non_boolean_values_in_it():

    query_string_parser = QueryStringParser(convert_string_to_number=True)

    query_dict = {
        'integer': 100,
        'codes': ['1', 'A', '2', '3', 'B']
    }

    expected_parsed_query_dict = {
        'integer': 100,
        'codes': ['1', 'A', '2', '3', 'B']
    }

    parsed_query_dict = query_string_parser.parse_dict(query_dict)

    assert expected_parsed_query_dict == parsed_query_dict

def test_query_dict_parser_converting_string_list_to_float_list():

    query_string_parser = QueryStringParser(convert_string_to_number=True, convert_number_only_to_float=True)

    query_dict = {
        'float': 100.0,
        'codes': [1, 2, 3]
    }

    expected_parsed_query_dict = {
        'float': 100.0,
        'codes': [1, 2, 3]
    }

    parsed_query_dict = query_string_parser.parse_dict(query_dict)

    assert expected_parsed_query_dict == parsed_query_dict

def test_query_dict_parser_converting_string_list_to_float_list_ignoring_field_codes():

    query_string_parser = QueryStringParser(convert_string_to_number=True, fields_to_number_to_ignore=['codes'], convert_number_only_to_float=True)

    query_dict = {
        'float': 100.0,
        'codes': ['1', '2', '3']
    }

    expected_parsed_query_dict = {
        'float': 100.0,
        'codes': ['1', '2', '3']
    }

    parsed_query_dict = query_string_parser.parse_dict(query_dict)

    assert expected_parsed_query_dict == parsed_query_dict

def test_query_dict_parser_without_convert_string_list_to_float_list():

    query_string_parser = QueryStringParser(convert_string_to_number=False, convert_number_only_to_float=True)

    query_dict = {
        'float': '100',
        'codes': ['1', '2', '3']
    }

    expected_parsed_query_dict = {
        'float': '100',
        'codes': ['1', '2', '3']
    }

    parsed_query_dict = query_string_parser.parse_dict(query_dict)

    assert expected_parsed_query_dict == parsed_query_dict

def test_query_dict_parser_not_converting_string_list_to_float_list_because_exists_non_boolean_values_in_it():

    query_string_parser = QueryStringParser(convert_string_to_number=True, convert_number_only_to_float=True)

    query_dict = {
        'float': 100,
        'codes': ['1', 'A', '2', '3', 'B']
    }

    expected_parsed_query_dict = {
        'float': 100,
        'codes': ['1', 'A', '2', '3', 'B']
    }

    parsed_query_dict = query_string_parser.parse_dict(query_dict)

    assert expected_parsed_query_dict == parsed_query_dict


def test_query_dict_parser_converting_string_list_to_number_list_considering_floats_and_ints():

    query_string_parser = QueryStringParser(convert_string_to_number=True)

    query_dict = {
        'sum': 100,
        'codes': [1, 2, 3],
        'vals': [1.0, 2.0, 3.0],
        'mix': [1, 2.0, 3, 4.0]
    }

    expected_parsed_query_dict = {
        'sum': 100,
        'codes': [1, 2, 3],
        'vals': [1.0, 2.0, 3.0],
        'mix': [1, 2.0, 3, 4.0]
    }

    parsed_query_dict = query_string_parser.parse_dict(query_dict)

    assert expected_parsed_query_dict == parsed_query_dict