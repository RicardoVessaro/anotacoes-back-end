import datetime
from api.modules.core.blueprints.service.note.note_validator import NoteValidator
from pytest import raises

class TestNoteValidator():

    def test_must_raise_exception_when_required_fields_are_not_given(self):
        validator = NoteValidator()
        
        body = {
	        "title": "teste",
            "pinned": True,
	        "text": "lorem ipsum dolor sit amet",
            "created_in": datetime.date.today()
        }

        for required_field in validator.required_fields:
            poped_value = body.pop(required_field)

            with raises(Exception, match=validator.REQUIRED_FIELD_EXCEPTION_MESSAGE.format(required_field)):
                validator.validate_insert(body)

            body[required_field] = poped_value

    def test_must_raise_exception_when_required_fields_are_None(self):
        validator = NoteValidator()
        
        body = {
	        "title": "teste",
            "pinned": True,
	        "text": "lorem ipsum dolor sit amet",
            "created_in": datetime.date.today()
        }

        for required_field in validator.required_fields:
            value = body[required_field]

            body[required_field] = None

            with raises(Exception, match=validator.REQUIRED_FIELD_EXCEPTION_MESSAGE.format(required_field)):
            
                validator.validate_insert(body)

            body[required_field] = value


    def test_must_raise_exception_when_required_fields_are_empty(self):
        validator = NoteValidator()
        
        body = {
	        "title": "teste",
            "pinned": True,
	        "text": "lorem ipsum dolor sit amet",
            "created_in": datetime.date.today()
        }

        for required_field in validator.required_fields:
            value = body[required_field]

            if(type(value) is str):
                body[required_field] = ""
            else: 
                body[required_field] = None

            with raises(Exception, match=validator.REQUIRED_FIELD_EXCEPTION_MESSAGE.format(required_field)):
            
                validator.validate_insert(body)

            body[required_field] = value