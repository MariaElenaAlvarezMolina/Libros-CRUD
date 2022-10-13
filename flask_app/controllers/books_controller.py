from flask_app import app
from flask import Flask, redirect, render_template, request
from flask_app.models.authors import Autor
from flask_app.models.books import Libro


@app.route('/libros')
def todos_los_libros():
    libros = Libro.mostrar_libros()
    return render_template('books.html', libros=libros)

@app.route('/crear/libro',methods=['POST'])
def crear_libro():
    formulario = {
        "título":request.form['título'],
        "num_páginas": request.form['num_páginas']
    }
    Libro.guardar(formulario)
    return redirect('/libros')

@app.route('/libro/<int:id>')
def mostrar_libro(id):
    formulario = {"id":id}
    libro = Libro.obtener_por_id(formulario)
    autores_sin_favorito = Autor.autores_sin_favoritos(formulario)
    return render_template('show_book.html', libro=libro, autores_sin_favorito=autores_sin_favorito)

@app.route('/guardar/autor',methods=['POST'])
def guardar_autor():
    formulario = {
        "autor_id": request.form['autor_id'],
        "libro_id": request.form['libro_id']
    }
    Autor.añadir_favorito(formulario)
    return redirect(f"/libro/{request.form['libro_id']}")