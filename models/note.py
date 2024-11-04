# models/note.py
from config.db import connectToMySQL
from datetime import datetime

class Note:
    def __init__(self, data):
        self.id = data['id']
        self.contenido = data['contenido']
        self.fecha_publicacion = data['fecha_publicacion']
        self.fecha_actualizacion = data.get('fecha_actualizacion')
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
        return connectToMySQL('lluvia').query_db(query, data)

    @classmethod
    def get_all(cls):
        query = """
        SELECT notes.*, users.nombre, users.apellido 
        FROM notes 
        JOIN users ON notes.user_id = users.id 
        ORDER BY notes.fecha_publicacion DESC;
        """
        results = connectToMySQL('lluvia').query_db(query)
        return results

    @classmethod
    def get_by_user_id(cls, user_id):
        query = """
        SELECT notes.*, users.nombre, users.apellido 
        FROM notes 
        JOIN users ON notes.user_id = users.id 
        WHERE notes.user_id = %(user_id)s 
        ORDER BY notes.fecha_publicacion DESC;
        """
        data = {'user_id': user_id}
        results = connectToMySQL('lluvia').query_db(query, data)
        return results

    @classmethod
    def update_one(cls, note_id, contenido):
        query = """
        UPDATE notes 
        SET contenido = %(contenido)s, fecha_actualizacion = NOW() 
        WHERE id = %(id)s;
        """
        data = {
            "contenido": contenido,
            "id": note_id
        }
        return connectToMySQL('lluvia').query_db(query, data)

    @classmethod
    def delete_one(cls, note_id):
        query = "DELETE FROM notes WHERE id = %(id)s;"
        data = {'id': note_id}
        return connectToMySQL('lluvia').query_db(query, data)

    @classmethod
    def get_by_id(cls, note_id):
        query = """
        SELECT notes.*, users.nombre, users.apellido 
        FROM notes 
        JOIN users ON notes.user_id = users.id 
        WHERE notes.id = %(id)s;
        """
        data = {'id': note_id}
        result = connectToMySQL('lluvia').query_db(query, data)
        return result[0] if result else None