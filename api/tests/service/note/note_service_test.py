
from unittest.mock import patch
from api.annotation.data.model.note import Note
from api.annotation.data.model.tag import Tag
from api.annotation.service.note.note_service import NoteService
from api.annotation.service.tag.tag_service import TagService
from ipsum.util.enviroment_variable import get_database_url
from ipsum.util.test.database_test import DatabaseTest

class TestNoteService:

    DB_URI = get_database_url()

    service = NoteService()

    dao = service._dao

    model = dao.model

    @patch.object(TagService, 'find_by_code')
    def test_must_insert_date_on_insert(self, mock_find_by_code):

        mock_tag = Tag(
            id='6248620366564103f229595f',
            code=100,
            name='Mock Tag',
            priority=4
        )

        mock_find_by_code.return_value = mock_tag

        database_test = DatabaseTest(host=self.DB_URI)
        @database_test.persistence_test()
        def _():
            def _test_dict():

                note = {
                    'pinned': True,
                    'text': "Test using dict"
                }

                inserted_note = self.service.insert(note)

                assert inserted_note.created_in is not None
                assert str(inserted_note.tag) == str(mock_tag.id)

            _test_dict()

            def _test_model():

                note = Note(
                    pinned=True,
                    text="Test using dict"
                )
                inserted_note = self.service.insert(note)

                assert inserted_note.created_in is not None

            _test_model()
        
        _()