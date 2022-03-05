
import datetime
from mongoengine import connect, disconnect
from pytest import raises
from api.modules.core.blueprints.data.model.note import Note
from api.modules.core.blueprints.service.note.note_service import NoteService

class TestNoteService:

    service = NoteService()

    model = service._dao._model

    # TODO criar estrutura generica para conexao nos testes
    def connect(self):
        DB_URI = "mongodb+srv://user:senha@anotacoes-cluster.jwtdf.mongodb.net/anotacoes-test?retryWrites=true&w=majority"
        connect(host=DB_URI)

    # TODO criar estrutura generica para conexao nos testes
    def disconnect(self):
        disconnect()

    # TODO criar estrutura gennerica para deletar documentos utilizados
    def clean_database(self, used_documents=[]):
        for document in used_documents:
            document.objects().delete()

    def test_insert(self):
        self.connect()
        self.clean_database(used_documents=[self.model])

        title = "test_insert_TestNoteService"

        note = {
	        "title": title,
            "pinned": True,
	        "text": "lorem ipsum dolor sit amet",
        }

        note_id = str(self.service.insert(note).id)
        note_bd = self.model.objects(title=title).first()
        assert str(note_bd.id) == note_id
        assert note_bd.created_in is not None

        note_bd.delete()
        self.disconnect()

    def test_find_by_id(self):
        self.connect()
        self.clean_database(used_documents=[self.model])

        title = "test_find_by_id_TestNoteService"

        note = {
	        "title": title,
            "pinned": True,
	        "text": "lorem ipsum dolor sit amet",
        }

        note_id = str(self.service.insert(note).id)
        note_bd = self.service.find_by_id(note_id)

        assert str(note_bd.id) == note_id
        assert note_bd.title == title

        note_bd.delete()
        self.disconnect()

    def test_delete(self):
        self.connect()
        self.clean_database(used_documents=[self.model])

        title = "test_delete_NoteService"

        note = {
	        "title": title,
            "pinned": True,
	        "text": "lorem ipsum dolor sit amet",
            "created_in": datetime.datetime.today()
        }

        note_id = str(self.service.insert(note).id)

        deleted_id = self.service.delete(note_id)

        assert deleted_id == note_id
        assert self.service.find_by_id(deleted_id) is None

        with raises(Exception, match=self.service._dao.OBJECT_NOT_FOUND_EXCEPTION_MESSAGE.format(deleted_id)):
            self.service.delete(deleted_id)

        self.disconnect()

    def test_must_remove_non_editable_fields(self):

        title = "test_must_remove_non_editable_fields_TestNoteService"

        note = {
            "title": title,
	        "text": "lorem ipsum dolor sit amet",
            "created_in": datetime.datetime.today()
        }

        editable_note = self.service._remove_non_editable_fields(note)

        assert "text" in editable_note

        for field in self.service._non_editable_fields:
            assert field not in editable_note     

    def test_update(self):
        self.connect()
        self.clean_database(used_documents=[self.model])

        note = {
	        "title": "test_update_NoteService ",
            "pinned": True,
	        "text": "lorem ipsum dolor sit amet",
        }

        note_id = str(self.service.insert(note).id)

        note_to_update = {
            "title": "test_update_NoteService Updated",
            "pinned": False,
	        "text": "lorem ipsum...",
            "created_in": None
        }

        updated_note = self.service.update(note_id, note_to_update)

        assert updated_note.title == note_to_update['title']
        assert updated_note.pinned == note_to_update['pinned']
        assert updated_note.text == note_to_update['text']
        assert updated_note.created_in.date() == note['created_in'].date()
        assert str(updated_note.id) == note_id

        updated_note.delete()

        self.disconnect()


    def test_find(self):
        self.connect()
        self.clean_database(used_documents=[self.model])

        note1 = {
	        "title": "test_find_NoteService 1",
            "pinned": True,
	        "text": "lorem ipsum dolor sit amet",
            "created_in": datetime.datetime.today()
        }

        note2 = {
	        "title": "test_find_NoteService 2",
            "pinned": False,
	        "text": "lorem ipsum dolor sit amet",
            "created_in": datetime.datetime.today()
        }

        note3 = {
	        "title": "test_find_NoteService 2",
            "pinned": True,
	        "text": "lorem ipsum dolor sit amet",
            "created_in": datetime.datetime.today()
        }

        note1_id = str(self.service.insert(note1).id)
        note2_id = str(self.service.insert(note2).id)
        note3_id = str(self.service.insert(note3).id)

        expected_found_ids = [note1_id, note3_id]

        query_filter = {
            "title": "test_find_NoteService 2",
            "pinned": True,
        }

        notes = self.service.find(query_filter)

        for note in notes:
            assert str(note.id) in expected_found_ids

        self.service.delete(note1_id)
        self.service.delete(note2_id)
        self.service.delete(note3_id)

        self.disconnect()

    def test_find_without_filter(self):
        self.connect()
        self.clean_database(used_documents=[self.model])

        note1 = {
	        "title": "test_find_NoteService 1",
            "pinned": True,
	        "text": "lorem ipsum dolor sit amet",
            "created_in": datetime.datetime.today()
        }

        note2 = {
	        "title": "test_find_NoteService 2",
            "pinned": False,
	        "text": "lorem ipsum dolor sit amet",
            "created_in": datetime.datetime.today()
        }

        note3 = {
	        "title": "test_find_NoteService 2",
            "pinned": True,
	        "text": "lorem ipsum dolor sit amet",
            "created_in": datetime.datetime.today()
        }

        note1_id = str(self.service.insert(note1).id)
        note2_id = str(self.service.insert(note2).id)
        note3_id = str(self.service.insert(note3).id)

        expected_found_ids = [note1_id, note2_id, note3_id]

        notes = self.service.find()

        for note in notes:
            assert str(note.id) in expected_found_ids

        self.service.delete(note1_id)
        self.service.delete(note2_id)
        self.service.delete(note3_id)

        self.disconnect()


    def test_paginate(self):
        self.connect()
        self.clean_database(used_documents=[self.model])

        notes, notes_id, pinned_notes_id = self._insert_notes()

        pagination = self.service.paginate()

        assert pagination['page'] == 1
        assert pagination['limit'] == 5
        assert pagination['total'] == 15
        assert pagination['has_prev'] == False
        assert pagination['has_next'] == True

        for item in pagination['items']:
            assert str(item.id) in notes_id[0:5]


        self.delete_notes(notes)
        self.disconnect()

    def test_paginate_with_filter(self):
        self.connect()
        self.clean_database(used_documents=[self.model])

        notes, notes_id, pinned_notes_id = self._insert_notes()

        pagination = self.service.paginate(query_filter={'pinned': False})

        assert pagination['page'] == 1
        assert pagination['limit'] == 5
        assert pagination['total'] == 15 - len(pinned_notes_id)
        assert pagination['has_prev'] == False
        assert pagination['has_next'] == True

        for item in pagination['items']:
            assert str(item.id) not in pinned_notes_id

        self.delete_notes(notes)
        self.disconnect()
    
    def test_paginate_limit_7_in_results(self):
        self.connect()
        self.clean_database(used_documents=[self.model])

        notes, notes_id, pinned_notes_id = self._insert_notes()

        pagination = self.service.paginate(limit=7)

        assert pagination['page'] == 1
        assert pagination['limit'] == 7
        assert pagination['total'] == 15
        assert pagination['has_prev'] == False
        assert pagination['has_next'] == True

        for item in pagination['items']:
            assert str(item.id) in notes_id[0:7]


        self.delete_notes(notes)
        self.disconnect()

    def test_paginate_limit_7_page_2_in_results(self):
        self.connect()
        self.clean_database(used_documents=[self.model])

        notes, notes_id, pinned_notes_id = self._insert_notes()

        pagination = self.service.paginate(limit=7, page=2)

        assert pagination['page'] == 2
        assert pagination['limit'] == 7
        assert pagination['total'] == 15
        assert pagination['has_prev'] == True
        assert pagination['has_next'] == True

        for item in pagination['items']:
            assert str(item.id) in notes_id[7:14]


        self.delete_notes(notes)
        self.disconnect()

    def test_paginate_limit_7_page_3_in_results(self):
        self.connect()
        self.clean_database(used_documents=[self.model])

        notes, notes_id, pinned_notes_id = self._insert_notes()

        pagination = self.service.paginate(limit=7, page=3)

        assert pagination['page'] == 3
        assert pagination['limit'] == 7
        assert pagination['total'] == 15
        assert pagination['has_prev'] == True
        assert pagination['has_next'] == False

        for item in pagination['items']:
            assert str(item.id) in notes_id[14:15]

        self.delete_notes(notes)
        self.disconnect()
    
    def test_paginate_must_raise_exception_when_page_is_greater_than_pages(self):
        self.connect()
        self.clean_database(used_documents=[self.model])

        notes, notes_id, pinned_notes_id = self._insert_notes()

        with raises(Exception, match=self.service._dao.PAGE_NOT_FOUND_EXCEPTION_MESSAGE.format(4, 3)):
            pagination = self.service.paginate(page=4, limit=5)

        self.delete_notes(notes)
        self.disconnect()

    def _insert_notes(self):
        notes = []
        notes_id = []
        pinned_notes_id = []

        pinned = True
        for i in range(15):
            note = {
	            "title": "test_paginate_NoteDAO " + str(i),
                "pinned": pinned,
	            "text": "lorem ipsum dolor sit amet",
                "created_in": datetime.datetime.today()
            }

            note_id = str(self.service.insert(note).id)

            note['id'] = note_id
    
            notes.append(note)
            notes_id.append(note_id)

            if pinned:
                pinned_notes_id.append(note_id)

            pinned = not pinned

        return notes, notes_id, pinned_notes_id

    def delete_notes(self, notes):
        for note in notes:
            self.service.delete(note['id'])