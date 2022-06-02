
from unicodedata import name
from unittest.mock import patch
import pytest
from api.modules.annotation.blueprints.data.model.note import Note
from api.modules.annotation.blueprints.data.model.tag import Tag
from api.modules.annotation.blueprints.service.note.note_service import NoteService
from api.modules.annotation.blueprints.service.tag.tag_service import TagService
from arq.util.enviroment_variable import get_test_database_url
from arq.util.test.database_test import DatabaseTest, clean_enums, insert_enums

class TestNoteService:

    DB_URI = get_test_database_url()

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

        arq_database_test = DatabaseTest(host=self.DB_URI)
        @arq_database_test.persistence_test()
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