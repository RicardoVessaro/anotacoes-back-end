from datetime import date, datetime
from bson import ObjectId
from flask.json import JSONEncoder
from mongoengine import Document
from json import dumps
from mongoengine.fields import BaseQuerySet
from flask_mongoengine import BaseQuerySet as FlaskBaseQuerySet

class ViewEncoder(JSONEncoder):

    KEY_ID = "_id"
    ID = "id"
    SUPPORTED_ITERATORS = [list, BaseQuerySet, FlaskBaseQuerySet]

    def default(self, o):

        return self._encode_object(o, use_default=True, dump_list=True)

    def _encode_object(self, o, use_default=False, dump_list=False):
        if o is None:
            return None

        if self._is_dict(o):
            return self._to_dict(o)

        if self._is_supported_iterator(o):
            return self._to_list(o, dump_list)

        if self._is_document(o):
            return self._to_mongo(o)

        if self._is_date(o):
            return self._to_isoformat(o)

        if self._is_object_id(o):
            return self._to_str(o)

        if not use_default:
            return o

        return super().default(o)

    def _is_dict(self, o):
        return type(o) is dict

    def _to_dict(self, o):
        o_dict = {}
        for key, value in o.items():
            encoded_value = self._encode_object(value)

            if key == self.KEY_ID:
                o_dict[self.ID] = encoded_value

            else :
                o_dict[key] = encoded_value

        return o_dict

    def _is_supported_iterator(self, o):
        return type(o) in self.SUPPORTED_ITERATORS

    def _to_list(self, o, dump_list=False):
        o_list = []

        for item in o:
            encoded_value = self._encode_object(item)

            o_list.append(encoded_value)

        if dump_list:
            return dumps(o_list)

        return o_list

    def _is_document(self, o):
        return isinstance(o, Document)

    def _to_mongo(self, o):
        o_mongo = o.to_mongo()

        return self._to_dict(o_mongo)

    def _is_date(self, o):
        return isinstance(o, (datetime, date))

    def _to_str(self, o):
        return str(o)

    def _is_object_id(self, o):
        return isinstance(o, ObjectId)

    def _to_isoformat(self, o):
        return o.isoformat()