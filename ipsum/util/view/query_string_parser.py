from urllib import parse

from ipsum.util.int_util import is_string_int
from ipsum.util.float_util import is_string_float
from ipsum.util.object_util import is_iterable

class QueryStringParser:

    IN = '[in]'
    NIN = '[nin]'
    AEQ = '[aeq]'

    LIST_OPERATORS = [
        IN, NIN, AEQ
    ]

    LIST_VALUES_SEPARATOR = '|'

    def __init__(self, convert_string_to_boolean=True, fields_to_boolean_to_ignore=[], convert_string_to_number=True, 
        fields_to_number_to_ignore=[], convert_number_only_to_float=False) -> None:

        self.convert_string_to_boolean = convert_string_to_boolean
        self.fields_to_boolean_to_ignore = fields_to_boolean_to_ignore
        self.convert_string_to_number = convert_string_to_number
        self.fields_to_number_to_ignore = fields_to_number_to_ignore
        self.convert_number_only_to_float = convert_number_only_to_float

    def parse_string(self, query_string:str) -> dict:
        parsed_query_string = parse.parse_qs(query_string)

        parsed_query_string = self._parse_query(parsed_query_string)

        return parsed_query_string

    def parse_dict(self, query_dict:dict) -> dict:
        parsed_query_string = self._transform_to_query(query_dict)

        parsed_query_string = self._parse_query(parsed_query_string)

        return parsed_query_string


    def _transform_to_query(self, query_dict:dict) -> dict:
        query = {}

        for key, value in query_dict.items():
            query[key] = value
            
            if not type(value) is list:
                query[key] = [value]

        return query


    def _parse_query(self, query) -> dict:
        query = self._decode_parsed_query_string(query)

        for key in query.keys():
            self._convert_string_list_values_to_list(query, key)

            self._convert_string_to_boolean(query, key)

            self._convert_string_to_number(query, key)

            self._convert_one_item_list_to_object(query, key)
            
        return query

    def _decode_parsed_query_string(self, parsed_query_string) -> dict:
        converted_parsed_query_string = {}
        
        B_TRUE = [b'True', b'true']
        B_FALSE = [b'False', b'false']

        for key in parsed_query_string:
            decoded_values = []

            for value in parsed_query_string[key]: 
                if type(value) is bytes:
                    if value in B_TRUE:
                        decoded_values.append('True')
                    
                    elif value in B_FALSE:
                        decoded_values.append('False')

                    else :
                        decoded_values.append(value.decode())

                else:
                    decoded_values.append(value)

            key_string = key 
            if type(key) is bytes:
                key_string = key.decode()

            converted_parsed_query_string[key_string] = decoded_values

        return converted_parsed_query_string

    def _convert_string_to_number(self, parsed_query_string, key):
        if self.convert_string_to_number and key not in self.fields_to_number_to_ignore:
            number_list = []
            for item in parsed_query_string[key]:
                if not self.convert_number_only_to_float and is_string_int(item):
                    number_list.append(int(item))

                elif is_string_float(item):
                    number_list.append(float(item))

            if len(number_list) == len(parsed_query_string[key]):
                parsed_query_string[key] = number_list

    def _convert_string_to_boolean(self, parsed_query_string, key):
        if self.convert_string_to_boolean:
            TRUE = ['true', 'True']

            FALSE = ['false', 'False']

            if key not in self.fields_to_boolean_to_ignore:
                value = parsed_query_string[key]

                boolean_list = []

                for item in value:
                    if item in TRUE:
                        boolean_list.append(True)

                    elif item in FALSE:
                        boolean_list.append(False)

                if len(boolean_list) == len(value):
                    parsed_query_string[key] = boolean_list

    def _convert_one_item_list_to_object(self, parsed_query_string, key):
        if len(parsed_query_string[key]) == 1 and not self._is_list_operation(key):
            parsed_query_string[key] = parsed_query_string[key][0]

    def _is_list_operation(self, key):
        for operator in self.LIST_OPERATORS:
            if operator in key:
                return True
                
        return False

    def _convert_string_list_values_to_list(self, parsed_query_string, key):

        if key not in self.fields_to_boolean_to_ignore:
            
            for value in parsed_query_string[key]:

                if is_iterable(value) and self.LIST_VALUES_SEPARATOR in value:
                    string_values = []

                    for string in value.split(self.LIST_VALUES_SEPARATOR):
                        string_without_spaces = string.split()

                        string_value = ''

                        for s in string_without_spaces:
                            string_value += s

                        string_values.append(string_value)
                
                    parsed_query_string[key] = string_values
