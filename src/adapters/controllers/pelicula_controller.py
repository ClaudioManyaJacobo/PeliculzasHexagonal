from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from src.adapters.repositories.pelicula_repository_sql import PeliculaRepositorySQL
from src.adapters.repositories.genero_repository_sql import GeneroRepositorySQL
from src.infrastructure.db import db

pelicula_bp = Blueprint('pelicula_bp', __name__)
pelicula_repo = PeliculaRepositorySQL(db)
genero_repo = GeneroRepositorySQL(db)


@pelicula_bp.route('/peliculas', methods=['GET'])
def obtener_peliculas():
    peliculas = pelicula_repo.obtener_todas_las_peliculas()

    # Crear una lista de diccionarios que incluye los géneros
    peliculas_con_generos = []
    for pelicula in peliculas:
        generos = [genero.name for genero in pelicula.generos]  # Obtener los nombres de los géneros asociados
        peliculas_con_generos.append({
            'id': pelicula.id,
            'nombre': pelicula.nombre,
            'anio': pelicula.anio,
            'sinopsis': pelicula.sinopsis,
            'duracion': pelicula.duracion,
            'director': pelicula.director,
            'generos': generos  # Lista de géneros de la película
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
        generos = request.form.getlist('generos')  # Lista de IDs de géneros seleccionados

        # Validación de los campos obligatorios
        if not nombre or not duracion or not sinopsis or not anio or not director or not generos:
            return jsonify({'error': 'Todos los campos son obligatorios'}), 400

        # Llamar al repositorio para agregar la película
        pelicula = pelicula_repo.agregar_pelicula(nombre, int(duracion), sinopsis, int(anio), director, generos)

        return redirect(url_for('pelicula_bp.obtener_peliculas'))  # Redirige a la lista de películas
    except Exception as e:
        return jsonify({'error': 'Error al agregar la película', 'detalle': str(e)}), 500
