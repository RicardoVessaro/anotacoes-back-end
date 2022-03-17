
# TODO Ver quando usar aspas simples ('') e aspas duplas ("")

# TODO Fazer com que o banco seja limpados dee forma automatica antes de iniciar os testes
# TODO Fazer com que os dados inseridos sejam cadastrados de forma automatica antes dos testes
# TODO Fazer com que os dados cadastrados sejam excluidos apos os testes

# TODO Fazer teste com uma entidade de testes

# TODO Rodar testes no kubernetes
# TODO Conectar ao banco de forma automatica

import datetime
from mongoengine import connect, disconnect
from bson import ObjectId
from pytest import raises
from api.modules.core.blueprints.service.note.note_service import NoteService
from arq.exception.arq_exception import ArqException
from arq.exception.arq_exception_message import OBJECT_NOT_FOUND_EXCEPTION_MESSAGE, PAGE_NOT_FOUND_EXCEPTION_MESSAGE
from arq.util.test.arq_test import ArqDatabaseTest
from api.modules.core.blueprints.data.model.note import Note

class TestNoteDAO():

    DB_URI = "mongodb+srv://user:senha@anotacoes-cluster.jwtdf.mongodb.net/anotacoes-test?retryWrites=true&w=majority"

    dao = NoteService()._dao
    
    # TODO ver se continua acessando atributo privado
    model = dao._model

    # TODO criar estrutura generica para conexao nos testes
    def connect(self):
        
        connect(host=self.DB_URI)

    # TODO criar estrutura generica para conexao nos testes
    def disconnect(self):
        disconnect()

    # TODO criar estrutura gennerica para deletar documentos utilizados
    def clean_database(self, used_documents=[]):
        for document in used_documents:
            document.objects().delete()
            
    def test_delete_arq_database_test(self):

        title = "test_delete_NoteDAO"

        note = Note(
            title=title,
            pinned=True,
            text="lorem ipsum dolor sit amet",
            created_in=datetime.datetime.today()
        )
        arq_database_test = ArqDatabaseTest()
        arq_database_test.add_data(self.dao, note)
        @arq_database_test.persistence_test(host=self.DB_URI)
        def test():
            note_id = str(note.id)

            deleted_id = self.dao.delete(note_id)

            assert deleted_id == note_id
            assert self.dao.find_by_id(deleted_id) is None
            

            with raises(ArqException, match=OBJECT_NOT_FOUND_EXCEPTION_MESSAGE.format(deleted_id)):
                self.dao.delete(deleted_id)

        test()
        

    def test_insert(self):
        self.connect()
        self.clean_database(used_documents=[self.model])

        title = "test_insert_NoteDAO"

        note = {
	        "title": title,
            "pinned": True,
	        "text": "lorem ipsum dolor sit amet",
            "created_in": datetime.datetime.today()
        }

        inserted_note = self.dao.insert(note)
        note_bd = self.model.objects(title=title).first()
        assert note_bd.id == inserted_note.id

        note_bd.delete()
        self.disconnect()

    def test_find_by_id(self):
        self.connect()
        self.clean_database(used_documents=[self.model])

        title = "test_find_by_id_NoteDAO"

        note = {
	        "title": title,
            "pinned": True,
	        "text": "lorem ipsum dolor sit amet",
            "created_in": datetime.datetime.today()
        }

        inserted_note = self.dao.insert(note)
        note_id = str(inserted_note.id)

        note_bd = self.dao.find_by_id(note_id)
        assert str(note_bd.id) == note_id
        assert note_bd.title == title

        note_bd = self.dao.find_by_id(ObjectId(note_id))
        assert str(note_bd.id) == note_id
        assert note_bd.title == title

        note_bd.delete()
        self.disconnect()


    def test_delete(self):
        self.connect()
        self.clean_database(used_documents=[self.model])

        title = "test_delete_NoteDAO"

        note = {
	        "title": title,
            "pinned": True,
	        "text": "lorem ipsum dolor sit amet",
            "created_in": datetime.datetime.today()
        }

        inserted_note = self.dao.insert(note)
        note_id = str(inserted_note.id)

        deleted_id = self.dao.delete(note_id)

        assert deleted_id == note_id
        assert self.dao.find_by_id(deleted_id) is None

        with raises(ArqException, match=OBJECT_NOT_FOUND_EXCEPTION_MESSAGE.format(deleted_id)):
            self.dao.delete(deleted_id)

        self.disconnect()


    def test_update(self):
        self.connect()
        self.clean_database(used_documents=[self.model])

        note = {
	        "title": "test_update_NoteDAO",
            "pinned": True,
	        "text": "lorem ipsum dolor sit amet",
            "created_in": datetime.datetime.today()
        }

        iserted_note = self.dao.insert(note)
        note_id = str(iserted_note.id)

        note_to_update = {
            "title": "test_update_NoteDAO Updated",
            "pinned": False,
	        "text": "lorem ipsum...",
        }

        updated_note = self.dao.update(note_id, note_to_update)

        assert updated_note.title == note_to_update['title']
        assert updated_note.pinned == note_to_update['pinned']
        assert updated_note.text == note_to_update['text']
        assert updated_note.created_in.date() == note['created_in'].date()
        assert str(updated_note.id) == note_id

        updated_note.delete()

        self.disconnect()

    # TODO testar com entidade que tem o valor de lista
    # TODO Com mais possibilidades com entidade especifica para testes
    def test_find(self):
        self.connect()
        self.clean_database(used_documents=[self.model])

        note1 = {
	        "title": "test_find_NoteDAO 1",
            "pinned": True,
	        "text": "lorem ipsum dolor sit amet",
            "created_in": datetime.datetime.today()
        }

        note2 = {
	        "title": "test_find_NoteDAO 2",
            "pinned": False,
	        "text": "lorem ipsum dolor sit amet",
            "created_in": datetime.datetime.today()
        }

        note3 = {
	        "title": "test_find_NoteDAO 2",
            "pinned": True,
	        "text": "lorem ipsum dolor sit amet",
            "created_in": datetime.datetime.today()
        }

        note1_id = str(self.dao.insert(note1).id)
        note2_id = str(self.dao.insert(note2).id)
        note3_id = str(self.dao.insert(note3).id)

        expected_found_ids = [note1_id, note3_id]

        query_filter = {
            "title": "test_find_NoteDAO 2",
            "pinned": True,
        }

        notes = self.dao.find(query_filter)

        for note in notes:
            assert str(note.id) in expected_found_ids

        self.dao.delete(note1_id)
        self.dao.delete(note2_id)
        self.dao.delete(note3_id)

        self.disconnect()

    def test_find_without_filter(self):
        self.connect()
        self.clean_database(used_documents=[self.model])

        note1 = {
	        "title": "test_find_NoteDAO 1",
            "pinned": True,
	        "text": "lorem ipsum dolor sit amet",
            "created_in": datetime.datetime.today()
        }

        note2 = {
	        "title": "test_find_NoteDAO 2",
            "pinned": False,
	        "text": "lorem ipsum dolor sit amet",
            "created_in": datetime.datetime.today()
        }

        note3 = {
	        "title": "test_find_NoteDAO 2",
            "pinned": True,
	        "text": "lorem ipsum dolor sit amet",
            "created_in": datetime.datetime.today()
        }

        note1_id = str(self.dao.insert(note1).id)
        note2_id = str(self.dao.insert(note2).id)
        note3_id = str(self.dao.insert(note3).id)

        expected_found_ids = [note1_id, note2_id, note3_id]

        notes = self.dao.find()

        for note in notes:
            assert str(note.id) in expected_found_ids

        self.dao.delete(note1_id)
        self.dao.delete(note2_id)
        self.dao.delete(note3_id)

        self.disconnect()

    def test_paginate(self):
        self.connect()
        self.clean_database(used_documents=[self.model])

        notes, notes_id, pinned_notes_id = self._insert_notes()

        pagination = self.dao.paginate()

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

        pagination = self.dao.paginate(query_filter={'pinned': False})

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

        pagination = self.dao.paginate(limit=7)

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
        notes, notes_id, pinned_notes_id = self._insert_notes()

        pagination = self.dao.paginate(limit=7, page=2)

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

        pagination = self.dao.paginate(limit=7, page=3)

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

        with raises(ArqException, match=PAGE_NOT_FOUND_EXCEPTION_MESSAGE.format(4, 3)):
            pagination = self.dao.paginate(page=4, limit=5)

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

            note_id = str(self.dao.insert(note).id)

            note['id'] = note_id
    
            notes.append(note)
            notes_id.append(note_id)

            if pinned:
                pinned_notes_id.append(note_id)

            pinned = not pinned

        return notes, notes_id, pinned_notes_id

    def delete_notes(self, notes):
        for note in notes:
            self.dao.delete(note['id'])
