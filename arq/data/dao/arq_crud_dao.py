
from arq.data.dao.arq_dao import ArqDao
from mongoengine import Document

from arq.exception.arq_exception import ArqException

class ArqCRUDDAO(ArqDao):

    OBJECT_NOT_FOUND_EXCEPTION_MESSAGE = "Object with ID {0} not found."

    def __init__(self, model:Document) -> None:
        super().__init__(model)

    def insert(self, model_data: dict) -> str:
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
            exception_message = self.OBJECT_NOT_FOUND_EXCEPTION_MESSAGE.format(id)
            raise ArqException(exception_message)

        deleted_id = model.id

        model.delete()

        return str(deleted_id)

