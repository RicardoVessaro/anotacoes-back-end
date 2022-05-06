
from api.modules.core.blueprints.data.model.note import Note
from api.modules.core.blueprints.service.note.note_service import NoteService
from arq.util.enviroment_variable import get_test_database_url
from arq.util.test.database_test import DatabaseTest

class TestNoteService:

    DB_URI = get_test_database_url()

    service = NoteService()

    dao = service._dao

    model = dao._model

    def test_must_insert_date_on_insert(self):
        arq_database_test = DatabaseTest(host=self.DB_URI, daos_to_clean=[self.dao])

        @arq_database_test.persistence_test()
        def _test_dict():

            note = {
                'pinned': True,
                'text': "Test using dict"
            }

            inserted_note = self.service.insert(note)

            assert inserted_note.created_in is not None

        _test_dict()

        @arq_database_test.persistence_test()
        def _test_model():

            note = Note(
                pinned=True,
                text="Test using dict"
            )

            inserted_note = self.service.insert(note)

            assert inserted_note.created_in is not None

        _test_model()
        