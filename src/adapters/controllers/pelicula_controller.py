from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from src.adapters.repositories.pelicula_repository_sql import PeliculaRepositorySQL
from src.adapters.repositories.genero_repository_sql import GeneroRepositorySQL
from src.infrastructure.db import db
import re
import base64

pelicula_bp = Blueprint('pelicula_bp', __name__)
pelicula_repo = PeliculaRepositorySQL(db)
genero_repo = GeneroRepositorySQL(db)

def convertir_a_embed(url):
    # Patrón para extraer el ID del video de diferentes tipos de URL
    youtube_pattern = (
        r"(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})|"
        r"(?:https?://)?(?:www\.)?youtu\.be/([a-zA-Z0-9_-]{11})|"
        r"(?:https?://)?(?:www\.)?youtube\.com/embed/([a-zA-Z0-9_-]{11})"
    )
    match = re.search(youtube_pattern, url)
    if match:
        # Extraer el ID del video (primer grupo coincidente)
        video_id = next(group for group in match.groups() if group)
        return f"https://www.youtube.com/embed/{video_id}"
    
    # Si no es una URL válida de YouTube, devuelve la original
    return url

@pelicula_bp.route('/peliculas', methods=['GET'])
def obtener_peliculas():
    peliculas = pelicula_repo.obtener_todas_las_peliculas()

    # Crear una lista de diccionarios que incluye los géneros y convierte la URL del video
    peliculas_con_generos = []
    for pelicula in peliculas:
        generos = [genero.name for genero in pelicula.generos]  # Obtener los nombres de los géneros asociados
        
        # Convertir la imagen binaria en base64, si existe
        imagen_base64 = None
        if pelicula.imagen:
            imagen_base64 = base64.b64encode(pelicula.imagen).decode('utf-8')  # Convertir los datos binarios a base64

        peliculas_con_generos.append({
            'id': pelicula.id,
            'nombre': pelicula.nombre,
            'anio': pelicula.anio,
            'sinopsis': pelicula.sinopsis,
            'duracion': pelicula.duracion,
            'director': pelicula.director,
            'url_video': convertir_a_embed(pelicula.url_video),  # Convertir la URL a formato embed
            'generos': generos,  # Lista de géneros de la película
            'imagen': imagen_base64  # Agregar la imagen en base64
        })
    
    return render_template('/peliculas/mostrar_peliculas.html', peliculas=peliculas_con_generos)

@pelicula_bp.route('/peliculas/agregar', methods=['GET'])
def mostrar_formulario_agregar():
    # Obtener todos los géneros disponibles
    generos = genero_repo.obtener_todos_los_generos()

    # Renderiza la plantilla y pasa los géneros como 'generos'
    return render_template('/peliculas/agregar_pelicula.html', generos=generos)

@pelicula_bp.route('/peliculas/agregar', methods=['POST'])
def agregar_pelicula():
    try:
        nombre = request.form.get('nombre')
        duracion = request.form.get('duracion')
        sinopsis = request.form.get('sinopsis')
        anio = request.form.get('anio')
        director = request.form.get('director')
        url_video = request.form.get('url_video')
        generos = request.form.getlist('generos')  # Lista de IDs de géneros seleccionados

        # Obtener la imagen cargada
        imagen = request.files['imagen']

        if imagen:
            imagen_binaria = imagen.read()  # Convertir la imagen a formato binario
        else:
            imagen_binaria = None
            print("No se ha recibido ninguna imagen")

        if not nombre or not duracion or not sinopsis or not anio or not director or not url_video or not generos:
            return jsonify({'error': 'Todos los campos son obligatorios'}), 400

        pelicula = pelicula_repo.agregar_pelicula(
            nombre, 
            int(duracion), 
            sinopsis, 
            int(anio), 
            director, 
            url_video, 
            generos, 
            imagen=imagen_binaria,  # Pasar la imagen binaria
        )
        imagen_binaria = imagen.read()
        print(f"Imagen leída: {imagen_binaria[:50]}...")  # Imprime los primeros 50 bytes para verificar

        return redirect(url_for('pelicula_bp.obtener_peliculas'))  # Redirige a la lista de películas
    
    except Exception as e:
        return jsonify({'error': 'Error al agregar la película', 'detalle': str(e)}), 500
    
