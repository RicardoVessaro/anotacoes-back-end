
from arq.data.dao.arq_dao import ArqDao
from mongoengine import Document

from arq.exception.arq_exception import ArqException
from arq.exception.arq_exception_message import OBJECT_NOT_FOUND_EXCEPTION_MESSAGE

class ArqCRUDDAO(ArqDao):

    def __init__(self, model:Document) -> None:
        super().__init__(model)

    def insert(self, model_data) -> str:
        # TODO testar usando model ao inves de dict
        model = model_data

        if type(model_data) is dict:
            model = self._model(**model_data)

        model.save()

        return model

    def update(self, id, model_date: dict):
        model = self.find_by_id(id)

        for key, value in model_date.items():
            model[key] = value

        return model.save()

    def delete(self, id):
        model = self.find_by_id(id)

        if model is None:
            exception_message = OBJECT_NOT_FOUND_EXCEPTION_MESSAGE.format(id)
            raise ArqException(exception_message, status_code=404)

        deleted_id = model.id

        model.delete()

        return str(deleted_id)

