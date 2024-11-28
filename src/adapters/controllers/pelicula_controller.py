from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from src.adapters.repositories.pelicula_repository_sql import PeliculaRepositorySQL
from src.adapters.repositories.genero_repository_sql import GeneroRepositorySQL
from src.infrastructure.db import db
import re
import base64

pelicula_bp = Blueprint('pelicula_bp', __name__)
pelicula_repo = PeliculaRepositorySQL(db)
genero_repo = GeneroRepositorySQL(db)

# Función para convertir la URL de YouTube a formato embed
def convertir_a_embed(url):
    youtube_pattern = (
        r"(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})|"
        r"(?:https?://)?(?:www\.)?youtu\.be/([a-zA-Z0-9_-]{11})|"
        r"(?:https?://)?(?:www\.)?youtube\.com/embed/([a-zA-Z0-9_-]{11})"
    )
    match = re.search(youtube_pattern, url)
    if match:
        video_id = next(filter(None, match.groups()), None)
        return f"https://www.youtube.com/embed/{video_id}"
    return url

# Función para validar campos obligatorios
def validar_campos_obligatorios(campos, datos):
    for campo in campos:
        if not datos.get(campo):
            return campo
    return None

# Función para manejar errores
def manejar_error(exception, mensaje="Error inesperado"):
    return render_template('error.html', error_message=str(exception), titulo="Error")

# Función para convertir una película a un formato dict
def convertir_pelicula_a_dict(pelicula):
    return {
        'id': pelicula.id,
        'nombre': pelicula.nombre,
        'anio': pelicula.anio,
        'sinopsis': pelicula.sinopsis,
        'duracion': pelicula.duracion,
        'director': pelicula.director,
        'url_video': convertir_a_embed(pelicula.url_video),
        'generos': [genero.name for genero in pelicula.generos],
        'imagen': base64.b64encode(pelicula.imagen).decode('utf-8') if pelicula.imagen else None
    }

# Rutas para obtener, agregar y eliminar películas
@pelicula_bp.route('/peliculas', methods=['GET'])
def obtener_peliculas():
    try:
        peliculas = pelicula_repo.obtener_todas_las_peliculas()
        peliculas_con_generos = [convertir_pelicula_a_dict(pelicula) for pelicula in peliculas]
        return render_template('/peliculas/index_peliculas.html', peliculas=peliculas_con_generos)
    except Exception as e:
        return manejar_error(e, "Error al cargar las películas")

@pelicula_bp.route('/peliculas/agregar', methods=['GET'])
def mostrar_formulario_agregar():
    try:
        generos = genero_repo.obtener_todos_los_generos()
        return render_template('/peliculas/add_peliculas.html', generos=generos)
    except Exception as e:
        return manejar_error(e, "Error al cargar el formulario")

@pelicula_bp.route('/peliculas/agregar', methods=['POST'])
def agregar_pelicula():
    try:
        campos_obligatorios = ['nombre', 'duracion', 'sinopsis', 'anio', 'director', 'url_video']
        faltante = validar_campos_obligatorios(campos_obligatorios, request.form)
        if faltante:
            return jsonify({'error': f'El campo {faltante} es obligatorio'}), 400

        nombre = request.form['nombre']
        duracion = int(request.form['duracion'])
        sinopsis = request.form['sinopsis']
        anio = int(request.form['anio'])
        director = request.form['director']
        url_video = request.form['url_video']
        generos = request.form.getlist('generos')
        imagen = request.files.get('imagen')
        imagen_binaria = imagen.read() if imagen else None

        pelicula_repo.agregar_pelicula(
            nombre, duracion, sinopsis, anio, director, url_video, generos, imagen=imagen_binaria
        )
        return redirect(url_for('pelicula_bp.obtener_peliculas'))
    
    except ValueError as e:
        return manejar_error(e, f"Ya existe una película con el nombre '{request.form['nombre']}'.")
    except Exception as e:
        return manejar_error(e, "Error al agregar la película")

@pelicula_bp.route('/peliculas/<int:pelicula_id>', methods=['GET'])
def mostrar_pelicula(pelicula_id):
    try:
        pelicula = pelicula_repo.obtener_pelicula_por_id(pelicula_id)
        if not pelicula:
            return render_template('error.html', mensaje="Película no encontrada")
        pelicula_dict = convertir_pelicula_a_dict(pelicula)
        return render_template('peliculas/show_pelicula.html', pelicula=pelicula_dict)
    except Exception as e:
        return manejar_error(e, "Error al cargar los detalles de la película")

@pelicula_bp.route('/peliculas/eliminar/<int:pelicula_id>', methods=['POST'])
def eliminar_pelicula(pelicula_id):
    try:
        pelicula = pelicula_repo.obtener_pelicula_por_id(pelicula_id)
        if not pelicula:
            return jsonify({'error': 'Película no encontrada'}), 404

        pelicula_repo.eliminar_pelicula(pelicula_id)
        db.session.commit()
        return redirect(url_for('pelicula_bp.obtener_peliculas'))
    except Exception as e:
        return manejar_error(e, "Error al eliminar la película")

@pelicula_bp.route('/peliculas/editar/<int:pelicula_id>', methods=['GET', 'POST'])
def editar_pelicula(pelicula_id):
    try:
        pelicula = pelicula_repo.obtener_pelicula_por_id(pelicula_id)
        if not pelicula:
            return manejar_error(ValueError("Película no encontrada"))

        if request.method == 'POST':
            campos_obligatorios = ['nombre', 'duracion', 'sinopsis', 'anio', 'director', 'url_video']
            faltante = validar_campos_obligatorios(campos_obligatorios, request.form)
            if faltante:
                return jsonify({'error': f'El campo {faltante} es obligatorio'}), 400

            nombre = request.form['nombre']
            duracion = int(request.form['duracion'])
            sinopsis = request.form['sinopsis']
            anio = int(request.form['anio'])
            director = request.form['director']
            url_video = request.form['url_video']
            generos = request.form.getlist('generos')
            imagen = request.files.get('imagen')
            imagen_binaria = imagen.read() if imagen else None

            pelicula_repo.editar_pelicula(
                pelicula_id,
                nombre=nombre,
                duracion=duracion,
                sinopsis=sinopsis,
                anio=anio,
                director=director,
                url_video=url_video,
                generos=generos,
                imagen=imagen_binaria
            )
            return redirect(url_for('pelicula_bp.obtener_peliculas'))

        # Si es un GET, mostramos el formulario con los datos existentes
        pelicula_dict = convertir_pelicula_a_dict(pelicula)
        generos = genero_repo.obtener_todos_los_generos()
        return render_template('/peliculas/edit_peliculas.html', pelicula=pelicula_dict, generos=generos)

    except Exception as e:
        return manejar_error(e, "Error al editar la película")