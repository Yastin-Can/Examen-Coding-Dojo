from config.db import connectToMySQL

class User:
    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.email = data['email']
        self.password = data['password']

    @classmethod
    def insert_one(cls, nombre, apellido, email, password):
        query = """
        INSERT INTO users (nombre, apellido, email, password)
        VALUES (%(nombre)s, %(apellido)s, %(email)s, %(password)s);
        """
        data = {
            "nombre": nombre,
            "apellido": apellido,
            "email": email,
            "password": password
        }
        result = connectToMySQL('lluvia').query_db(query, data)
        return result

    @classmethod
    def get_by_email(cls, email):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        data = {'email': email}
        result = connectToMySQL('lluvia').query_db(query, data)
        return cls(result[0]) if result else None

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('lluvia').query_db(query)
        return [cls(user) for user in results] if results else []
