
import json
from dateutil.parser import isoparse
from arq.util.view.view_encoder import ViewEncoder
from bson import ObjectId

from arq.tests.resources.data.model.arq_test_model import ArqTestModel


class TestViewEncoder:

    def test_date_encode(self):

        iso_format_date = "2022-03-05T15:49:22.507352"
        test_date = isoparse(iso_format_date)

        view_encoder = ViewEncoder()
        encoded_date = view_encoder.default(test_date)

        assert encoded_date == iso_format_date

    def test_object_id_encode(self):

        id = "507f191e810c19729de860ea"
        object_id = ObjectId(id)

        view_encoder = ViewEncoder()
        encoded_id = view_encoder.default(object_id)

        assert encoded_id == id

    def test_document_encode(self):

        id = "507f191e810c19729de860ea"
        document_id = ObjectId(id)

        text = " lorem ipsum"
        title = "Doc"
        code = 1

        test_model = ArqTestModel(id=document_id, code=code, title=title, boolean=True, tags=['A', 'B', 'C'])

        expected_encoded_doc = {
            "id": id,
            "code": code,
            "title": title,
            "boolean": True,
            "tags": ['A', 'B', 'C']
        }

        assert expected_encoded_doc == ViewEncoder().default(test_model)

    def test_list_encode(self):

        iso_format_day = "2022-03-05T15:49:22.507352"
        day = isoparse(iso_format_day)

        id = "507f191e810c19729de860ea"
        document_id = ObjectId(id)

        text = "text"

        list_id = "507f191e810c19729de970bc"
        object_list_id = ObjectId(list_id)

        test_list = [day, document_id, text, [object_list_id]]

        expected_list = [iso_format_day, id, text, [list_id]]

        encoded_list = ViewEncoder().default(test_list)
        from_json_encoded_list = json.loads(encoded_list)

        assert expected_list == from_json_encoded_list

    def test_dict_encode(self):

        iso_format_day = "2022-03-05T15:49:22.507352"
        day = isoparse(iso_format_day)

        id = "507f191e810c19729de860ea"
        document_id = ObjectId(id)

        text = "lorem"
        name = "dict"

        dict_id = "507f191e810c19729de970bc"
        object_dict_id = ObjectId(dict_id)

        test_dict = {
            "_id": object_dict_id,
            "day": day,
            "other_dict": {
                "name": name,
                "text": text,
                "list": ['A', 'B', 'C']
            }
        }

        expected_dict = {
            "id": dict_id,
            "day": iso_format_day,
            "other_dict": {
                "name": name,
                "text": text,
                "list": ['A', 'B', 'C']
            }
        }

        encoded_dict = ViewEncoder().default(test_dict)

        assert expected_dict == encoded_dict

    def test_none_encode(self):

        assert ViewEncoder().default(None) is None
