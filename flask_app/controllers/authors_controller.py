from flask import Flask, render_template, request, redirect
from flask_app import app
from flask_app.models.authors import Autor
from flask_app.models.books import Libro

@app.route('/')
def index():
    autores = Autor.mostrar_autores()
    return render_template('authors.html', autores=autores)

@app.route('/crear/autor', methods=['POST'])
def crear_autor():
    formulario = {"nombre": request.form['nombre']}
    Autor.guardar_autor(formulario)
    return redirect('/')

@app.route('/autor/<int:id>')
def mostrar_autor(id):
    formulario = {"id": id}
    autor = Autor.obtener_por_id(formulario)
    no_favorito = Libro.no_favorito(formulario)
    return render_template('show_author.html', autor=autor, no_favorito=no_favorito)

@app.route('/guardar/libro',methods=['POST'])
def guardar_libro():
    formulario = {
        "autor_id": request.form['autor_id'],
        "libro_id": request.form['libro_id']
        }
    Autor.añadir_favorito(formulario)
    return redirect(f"/autor/{request.form['autor_id']}")