from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from src.adapters.repositories.pelicula_repository_sql import PeliculaRepositorySQL
from src.infrastructure.db import db

pelicula_bp = Blueprint('pelicula_bp', __name__)
pelicula_repo = PeliculaRepositorySQL(db)


@pelicula_bp.route('/peliculas', methods=['GET'])
def obtener_peliculas():
    peliculas = pelicula_repo.obtener_todas_las_peliculas()
    return render_template('mostrar_peliculas.html', peliculas=peliculas)


@pelicula_bp.route('/peliculas/agregar', methods=['GET'])
def mostrar_formulario_agregar():
    return render_template('agregar_pelicula.html')

@pelicula_bp.route('/peliculas/agregar', methods=['POST'])
def agregar_pelicula():
    try:
        nombre = request.form.get('nombre')
        duracion = request.form.get('duracion')
        sinopsis = request.form.get('sinopsis')
        anio = request.form.get('anio')
        director = request.form.get('director')


        if not nombre or not duracion or not sinopsis or not anio or not director:
            return jsonify({'error': 'Todos los campos son obligatorios'}), 400

        pelicula = pelicula_repo.agregar_pelicula(nombre, int(duracion), sinopsis, int(anio), director)
        return redirect(url_for('pelicula_bp.obtener_peliculas'))  # Redirige a la lista de películas
    except Exception as e:
        return jsonify({'error': 'Error al agregar la película', 'detalle': str(e)}), 500
