
from xmlrpc.client import boolean
from pytest import raises
from arq.exception.exception_message import REQUIRED_FIELD_EXCEPTION_MESSAGE
from arq.service.crud_validator import CRUDValidator
from arq.exception.arq_exception import ArqException
from arq.tests.resources.data.model.arq_test_model import ArqTestModel

class TestArqCRUDValidator:

    arq_crud_validator = CRUDValidator(required_fields=['code', 'title'])

    def test_validate_insert(self):

        def test_using_dict_when_required_fields_are_not_given():

            body = {
                'code': 1,
                'title': 'test_validate_insert_ArqCRUDValidator',
                'boolean': True,
                'tag': ['A', 'B']
            }

            for required_field in self.arq_crud_validator.required_fields:
                poped_value = body.pop(required_field)

                with raises(ArqException, match=REQUIRED_FIELD_EXCEPTION_MESSAGE.format(required_field)):
                    self.arq_crud_validator.validate_insert(body)

                body[required_field] = poped_value

        test_using_dict_when_required_fields_are_not_given()

        def test_using_dict_when_required_fields_are_empty():

            body = {
                'code': 1,
                'title': 'test_validate_insert_ArqCRUDValidator',
                'boolean': True,
                'tag': ['A', 'B']
            }

            for required_field in self.arq_crud_validator.required_fields:
                value = body[required_field]

                body[required_field] = None

                with raises(ArqException, match=REQUIRED_FIELD_EXCEPTION_MESSAGE.format(required_field)):
                    self.arq_crud_validator.validate_insert(body)

                body[required_field] = value

        test_using_dict_when_required_fields_are_empty()

        def test_using_model():

            model = ArqTestModel(
                code=1,
                title='test_validate_insert_ArqCRUDValidator',
                boolean=True,
                tags=['A', 'B']
            )

            for required_field in self.arq_crud_validator.required_fields:
                poped_value = model[required_field]
                model[required_field] = None

                with raises(ArqException, match=REQUIRED_FIELD_EXCEPTION_MESSAGE.format(required_field)):
                    self.arq_crud_validator.validate_insert(model)

                model[required_field] = poped_value

        test_using_model()

    def test_update(self):

        def test_must_raise_exception_when_required_fields_are_empty_on_update_using_dict():
            fake_id = "12AB3CD4"
            
            body = {
                "title": None,
                "pinned": True,
                "text": "lorem ipsum dolor sit amet"
            }

            for field in body.keys():
                if field in self.arq_crud_validator.required_fields:
                    value = body[field]

                    body[field] = None

                    with raises(ArqException, match=REQUIRED_FIELD_EXCEPTION_MESSAGE.format(field)):
                        self.arq_crud_validator.validate_update(fake_id, body)

                    body[field] = value

        test_must_raise_exception_when_required_fields_are_empty_on_update_using_dict()

        def test_must_raise_exception_when_required_fields_are_empty_on_update_using_model():

            fake_id = "12AB3CD4"
        
            model = ArqTestModel(
                code=1, 
                title='test_update_ArqCRUDValidator',
            )

            for field in model.to_mongo().keys():
                if field in self.arq_crud_validator.required_fields:
                    value = model[field]

                    model[field] = None

                    with raises(ArqException, match=REQUIRED_FIELD_EXCEPTION_MESSAGE.format(field)):
                        self.arq_crud_validator.validate_update(fake_id, model)

                    model[field] = value

        test_must_raise_exception_when_required_fields_are_empty_on_update_using_model()

