from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import authors

class Libro:
    def __init__(self, data):
        self.id = data['id']
        self.título = data['título']
        self.num_páginas = data['num_páginas']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.autores_que_marcaron_favorito = []
    

    @classmethod
    def mostrar_libros(cls):
        query = "SELECT * FROM libros"
        results = connectToMySQL('libros_crud').query_db(query)
        libros = []
        for libro in results:
            libros.append(cls(libro))
        return libros
    
    @classmethod
    def guardar(cls, formulario):
        query = "INSERT INTO libros (título, num_páginas) VALUES (%(título)s,%(num_páginas)s)"
        result = connectToMySQL('libros_crud').query_db(query, formulario)
        return result

    @classmethod
    def obtener_por_id(cls, formulario):
        query = "SELECT * FROM libros LEFT JOIN favoritos ON libros.id = favoritos.libro_id LEFT JOIN autores ON autores.id = favoritos.autor_id WHERE libros.id = %(id)s"
        results = connectToMySQL('libros_crud').query_db(query, formulario)

        libro = cls(results[0])
        for row in results:
            if row['autores.id'] == None:
                break
            formulario = {
                "id": row['autores.id'],
                "nombre": row['nombre'],
                "created_at": row['autores.created_at'],
                "updated_at": row['autores.updated_at']
            }
            libro.autores_que_marcaron_favorito.append(authors.Autor(formulario))
        return libro

    @classmethod
    def no_favorito(cls, formulario):
        query = "SELECT * FROM libros WHERE libros.id NOT IN ( SELECT libro_id FROM favoritos WHERE autor_id = %(id)s )"
        results = connectToMySQL('libros_crud').query_db(query, formulario)
        libros = []
        for libro in results:
            libros.append(cls(libro))
        return libros