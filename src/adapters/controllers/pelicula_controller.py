from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from src.adapters.repositories.pelicula_repository_sql import PeliculaRepositorySQL
from src.adapters.repositories.genero_repository_sql import GeneroRepositorySQL
from src.adapters.repositories.actor_repository_sql import ActorRepositorySQL
from src.infrastructure.db import db
import re
import base64


# Crear el Blueprint para manejar las rutas relacionadas con las películas
pelicula_bp = Blueprint('pelicula_bp', __name__)
pelicula_repo = PeliculaRepositorySQL(db)
genero_repo = GeneroRepositorySQL(db)
actor_repo = ActorRepositorySQL(db)

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
        'actores': [actor.nombre for actor in pelicula.actores],
        'imagen': base64.b64encode(pelicula.imagen).decode('utf-8') if pelicula.imagen else None
    }

##########LAS#########
######## RUTAS########

# Ruta para obtener todas las películas y mostrarlas en la página de inicio
@pelicula_bp.route('/peliculas', methods=['GET'])
def obtener_peliculas():
    peliculas = pelicula_repo.obtener_todas_las_peliculas()
    peliculas_con_generos = [convertir_pelicula_a_dict(pelicula) for pelicula in peliculas]
    return render_template('/peliculas/index_peliculas.html', peliculas=peliculas_con_generos)


# Ruta para mostrar el formulario de adición de una nueva película
@pelicula_bp.route('/peliculas/agregar', methods=['GET'])
def mostrar_formulario_agregar():
    generos = genero_repo.obtener_todos_los_generos()
    actores = actor_repo.obtener_todos_los_actores()
    return render_template('/peliculas/add_peliculas.html', generos=generos, actores=actores)


@pelicula_bp.route('/peliculas/agregar', methods=['POST'])
def agregar_pelicula():
    # Verifica si todos los campos obligatorios están presentes
    campos_obligatorios = ['nombre', 'duracion', 'sinopsis', 'anio', 'director', 'url_video']
    faltante = validar_campos_obligatorios(campos_obligatorios, request.form)
    if faltante:
        return jsonify({'error': f'El campo {faltante} es obligatorio'}), 400

    # Obtiene los datos del formulario
    nombre = request.form['nombre']
    try:
        duracion = int(request.form['duracion'])
        anio = int(request.form['anio'])
    except ValueError:
        return jsonify({'error': 'La duración y el año deben ser números válidos'}), 400

    sinopsis = request.form['sinopsis']
    director = request.form['director']
    url_video = request.form['url_video']
    generos = [int(id) for id in request.form.getlist('generos')]
    imagen = request.files.get('imagen')
    imagen_binaria = imagen.read() if imagen else None
    actores = [int(id) for id in request.form.getlist('actores')]

    # Llama al repositorio para agregar la película
    pelicula_repo.agregar_pelicula(
        nombre, duracion, sinopsis, anio, director, url_video, generos, imagen=imagen_binaria, actores=actores
    )

    return redirect(url_for('pelicula_bp.obtener_peliculas'))


# Ruta para mostrar los detalles de una película específica
@pelicula_bp.route('/peliculas/<int:pelicula_id>', methods=['GET'])
def mostrar_pelicula(pelicula_id):
    # Busca la película por ID
    pelicula = pelicula_repo.obtener_pelicula_por_id(pelicula_id)
    if not pelicula:
        # Devuelve una página de error si no se encuentra la película
        return render_template('error.html', mensaje="Película no encontrada")
    
    # Convierte la película a un formato dict y la pasa a la plantilla
    pelicula_dict = convertir_pelicula_a_dict(pelicula)
    return render_template('peliculas/show_pelicula.html', pelicula=pelicula_dict)


# Ruta para eliminar una película de la base de datos
@pelicula_bp.route('/peliculas/eliminar/<int:pelicula_id>', methods=['POST'])
def eliminar_pelicula(pelicula_id):
    # Busca la película por ID
    pelicula = pelicula_repo.obtener_pelicula_por_id(pelicula_id)
    if not pelicula:
        return jsonify({'error': 'Película no encontrada'}), 404

    # Elimina la película y confirma la operación
    pelicula_repo.eliminar_pelicula(pelicula_id)
    db.session.commit()

    # Redirige a la lista de películas
    return redirect(url_for('pelicula_bp.obtener_peliculas'))


# Ruta para mostrar el formulario de edición de una película y manejar la actualización
@pelicula_bp.route('/peliculas/editar/<int:pelicula_id>', methods=['GET', 'POST'])
def editar_pelicula(pelicula_id):
    try:
        pelicula = pelicula_repo.obtener_pelicula_por_id(pelicula_id)
        if not pelicula:
            # Redirige al método de manejo de errores global con un mensaje específico
            return redirect(url_for('error_page', error_message="Película no encontrada"))

        if request.method == 'POST':
            campos_obligatorios = ['nombre', 'duracion', 'sinopsis', 'anio', 'director', 'url_video']
            faltante = validar_campos_obligatorios(campos_obligatorios, request.form)
            if faltante:
                # Redirige al método de manejo de errores global si falta un campo obligatorio
                return redirect(url_for('error_page', error_message=f'El campo {faltante} es obligatorio'))

            nombre = request.form['nombre']
            duracion = int(request.form['duracion'])
            sinopsis = request.form['sinopsis']
            anio = int(request.form['anio'])
            director = request.form['director']
            url_video = request.form['url_video']
            generos = request.form.getlist('generos')
            actores = request.form.getlist('actores')
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
                actores=actores,
                imagen=imagen_binaria
            )
            return redirect(url_for('pelicula_bp.obtener_peliculas'))

        # Si es un GET, mostramos el formulario con los datos existentes
        pelicula_dict = convertir_pelicula_a_dict(pelicula)
        generos = genero_repo.obtener_todos_los_generos()
        actores = actor_repo.obtener_todos_los_actores()
        return render_template('/peliculas/edit_peliculas.html', pelicula=pelicula_dict, generos=generos, actores=actores)

    except Exception as e:
        # Redirige al método de manejo de errores global con el mensaje de error
        return redirect(url_for('error_page', error_message=f"Error al editar la película: {str(e)}"))
