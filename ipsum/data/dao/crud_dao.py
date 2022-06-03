
from ipsum.data.dao.dao import DAO
from mongoengine import Document

from ipsum.exception.ipsum_exception import IpsumException
from ipsum.exception.exception_message import OBJECT_NOT_FOUND_EXCEPTION_MESSAGE

class CRUDDAO(DAO):

    def __init__(self, model:Document) -> None:
        super().__init__(model)

    def insert(self, model_data, **kwargs) -> str:
        model = model_data

        if type(model_data) is dict:
            model = self._model(**model_data)

        model.save(**kwargs)

        return model

    def update(self, id, model_data, **kwargs):
        if self.find_by_id(id) is None:
            exception_message = OBJECT_NOT_FOUND_EXCEPTION_MESSAGE.format(id)
            raise IpsumException(exception_message, status_code=404)
            
        model = model_data
        
        if type(model_data) is dict:
            model = self.find_by_id(id)

            for key, value in model_data.items():
                model[key] = value

        return model.save(**kwargs)

    def delete(self, id):
        model = self.find_by_id(id)

        if model is None:
            exception_message = OBJECT_NOT_FOUND_EXCEPTION_MESSAGE.format(id)
            raise IpsumException(exception_message, status_code=404)

        deleted_id = model.id

        model.delete()

        return str(deleted_id)

