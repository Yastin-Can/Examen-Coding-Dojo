# models/note.py
from config.db import connectToMySQL

class Note:
    def __init__(self, data):
        self.id = data['id']
        self.contenido = data['contenido']
        self.fecha_publicacion = data['fecha_publicacion']
        self.user_id = data['user_id']

    @classmethod
    def insert_one(cls, contenido, user_id):
        query = """
        INSERT INTO notes (contenido, user_id)
        VALUES (%(contenido)s, %(user_id)s);
        """
        data = {
            "contenido": contenido,
            "user_id": user_id
        }
        result = connectToMySQL('lluvia').query_db(query, data)
        return result

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM notes;"
        results = connectToMySQL('lluvia').query_db(query)
        return [cls(note) for note in results] if results else []

    @classmethod
    def get_by_user_id(cls, user_id):
        query = "SELECT * FROM notes WHERE user_id = %(user_id)s;"
        data = {'user_id': user_id}
        results = connectToMySQL('lluvia').query_db(query, data)
        return [cls(note) for note in results] if results else []

    @classmethod
    def update_one(cls, note_id, contenido):
        query = """
        UPDATE notes SET contenido = %(contenido)s WHERE id = %(id)s;
        """
        data = {
            "contenido": contenido,
            "id": note_id
        }
        result = connectToMySQL('lluvia').query_db(query, data)
        return result

    @classmethod
    def delete_one(cls, note_id):
        query = "DELETE FROM notes WHERE id = %(id)s;"
        data = {'id': note_id}
        result = connectToMySQL('lluvia').query_db(query, data)
        return result
