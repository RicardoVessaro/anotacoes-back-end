import datetime
from api.modules.core.blueprints.service.note.note_validator import NoteValidator
from pytest import raises

from arq.exception.arq_exception import ArqException

class TestNoteValidator():

    _validator = NoteValidator()

    def test_must_raise_exception_when_required_fields_are_not_given_on_insert(self):
        
        body = {
	        "title": "teste",
            "pinned": True,
	        "text": "lorem ipsum dolor sit amet",
            "created_in": datetime.date.today()
        }

        for required_field in self._validator.required_fields:
            poped_value = body.pop(required_field)

            with raises(ArqException, match=self._validator.REQUIRED_FIELD_EXCEPTION_MESSAGE.format(required_field)):
                self._validator.validate_insert(body)

            body[required_field] = poped_value

    def test_must_raise_exception_when_required_fields_are_none_on_insert(self):
        
        body = {
	        "title": "teste",
            "pinned": True,
	        "text": "lorem ipsum dolor sit amet",
            "created_in": datetime.date.today()
        }

        for required_field in self._validator.required_fields:
            value = body[required_field]

            body[required_field] = None

            with raises(ArqException, match=self._validator.REQUIRED_FIELD_EXCEPTION_MESSAGE.format(required_field)):
            
                self._validator.validate_insert(body)

            body[required_field] = value


    def test_must_raise_exception_when_required_fields_are_empty_on_insert(self):
        
        body = {
	        "title": "teste",
            "pinned": True,
	        "text": "lorem ipsum dolor sit amet",
            "created_in": datetime.date.today()
        }

        for required_field in self._validator.required_fields:
            value = body[required_field]

            if(type(value) is str):
                body[required_field] = ""
            else: 
                body[required_field] = None

            with raises(ArqException, match=self._validator.REQUIRED_FIELD_EXCEPTION_MESSAGE.format(required_field)):
            
                self._validator.validate_insert(body)

            body[required_field] = value

    def test_must_raise_exception_when_required_fields_are_empty_on_update(self):
        fake_id = "12AB3CD4"
        
        body = {
	        "title": None,
            "pinned": True,
	        "text": "lorem ipsum dolor sit amet"
        }

        for field in body.keys():
            if field in self._validator.required_fields:
                value = body[field]

                body[field] = None

                with raises(ArqException, match=self._validator.REQUIRED_FIELD_EXCEPTION_MESSAGE.format(field)):
                    self._validator.validate_update(fake_id, body)

                body[field] = value

