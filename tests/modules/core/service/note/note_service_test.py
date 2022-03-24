
from api.modules.core.blueprints.data.model.note import Note
from api.modules.core.blueprints.service.note.note_service import NoteService
from arq.util.test.arq_database_test import ArqDatabaseTest

# TODO Usar URI por variavel de ambiente ao inves de TEST_DB_URI

class TestNoteService:

    DB_URI = "mongodb+srv://user:senha@anotacoes-cluster.jwtdf.mongodb.net/anotacoes-test?retryWrites=true&w=majority"

    service = NoteService()

    dao = service._dao

    model = dao._model

    def test_must_insert_date_on_insert(self):
        arq_database_test = ArqDatabaseTest(daos_to_clean=[self.dao])

        @arq_database_test.persistence_test(host=self.DB_URI)
        def _test_dict():

            note = {
                'pinned': True,
                'text': "Test using dict"
            }

            inserted_note = self.service.insert(note)

            assert inserted_note.created_in is not None

        _test_dict()

        @arq_database_test.persistence_test(host=self.DB_URI)
        def _test_model():

            note = Note(
                pinned=True,
                text="Test using dict"
            )

            inserted_note = self.service.insert(note)

            assert inserted_note.created_in is not None

        _test_model()
        