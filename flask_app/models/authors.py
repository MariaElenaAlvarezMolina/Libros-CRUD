from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import books

class Autor:
    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.libros_favoritos = []


    @classmethod
    def guardar_autor(cls, formulario):
        query = "INSERT INTO autores (nombre) VALUES (%(nombre)s)"
        result = connectToMySQL('libros_crud').query_db(query, formulario)
        return result

    @classmethod
    def mostrar_autores(cls):
        query = "SELECT * FROM autores"
        results = connectToMySQL('libros_crud').query_db(query)
        autores = []
        for autor in results:
            autores.append(cls(autor))
        return autores

    @classmethod
    def autores_sin_favoritos(cls, formulario):
        query = "SELECT * FROM autores WHERE autores.id NOT IN ( SELECT autor_id FROM favoritos WHERE libro_id = %(id)s )"
        results = connectToMySQL('libros_crud').query_db(query, formulario)
        autores = []
        for autor in results:
            autores.append(cls(autor))
        return autores

    @classmethod
    def añadir_favorito(cls, formulario):
        query = "INSERT INTO favoritos (autor_id, libro_id) VALUES (%(autor_id)s, %(libro_id)s)"
        result = connectToMySQL('libros_crud').query_db(query, formulario)
        return result

    @classmethod
    def obtener_por_id(cls, formulario):
        query = "SELECT * FROM autores LEFT JOIN favoritos ON autores.id = favoritos.autor_id LEFT JOIN libros ON libros.id = favoritos.libro_id WHERE autores.id = %(id)s"
        results = connectToMySQL('libros_crud').query_db(query, formulario)

        autor = cls(results[0])
        for row in results:
            if row['libros.id'] == None:
                break
            formulario = {
                "id": row['libros.id'],
                "título": row['título'],
                "num_páginas": row['num_páginas'],
                "created_at": row['libros.created_at'],
                "updated_at": row['libros.updated_at']
            }
            autor.libros_favoritos.append(books.Libro(formulario))
        return autor