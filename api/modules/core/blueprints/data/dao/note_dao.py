
from api.modules.core.blueprints.data.model.note import Note

class NoteDao:

    def __init__(self) -> None:
        self._model = Note

    def insert(self, model_data: dict) -> str:
        model = self._model(**model_data)
        model.save()

        return str(model.id)

    """
    find
    find_all
    find_paginated
    update
    delete
    """
    
   
