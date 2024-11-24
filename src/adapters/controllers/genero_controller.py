from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from src.adapters.repositories.genero_repository_sql import GeneroRepositorySQL
from src.infrastructure.db import db

genero_bp = Blueprint('genero_bp', __name__)
genero_repo = GeneroRepositorySQL(db)

@genero_bp.route('/generos', methods=['GET'])
def obtener_generos():
    generos = genero_repo.obtener_todos_los_generos()
    return render_template('/generos/mostrar_generos.html', generos=generos)

@genero_bp.route('/generos/agregar', methods=['GET'])
def mostrar_formulario_agregar():
    return render_template('/generos/agregar_genero.html')

@genero_bp.route('/generos/agregar', methods=['POST'])
def agregar_genero():
    try:
        name = request.form.get('name')

        if not name:
            return jsonify({'error': 'El nombre del género es obligatorio'}), 400

        genero = genero_repo.agregar_genero(name)
        return redirect(url_for('genero_bp.obtener_generos'))  # Redirige a la lista de géneros
    except Exception as e:
        return jsonify({'error': 'Error al agregar el género', 'detalle': str(e)}), 500