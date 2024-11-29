from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from src.adapters.repositories.genero_repository_sql import GeneroRepositorySQL
from src.infrastructure.db import db

genero_bp = Blueprint('genero_bp', __name__)
genero_repo = GeneroRepositorySQL(db)


@genero_bp.route('/generos', methods=['GET'])
def obtener_generos():
    generos = genero_repo.obtener_todos_los_generos()
    return render_template('generos/index_generos.html', generos=generos)

@genero_bp.route('/generos/agregar', methods=['GET'])
def mostrar_formulario_agregar():
    return render_template('generos/add_generos.html')

@genero_bp.route('/generos/agregar', methods=['POST'])
def agregar_genero():
    try:
        # Obtener el nombre del género desde el formulario
        name = request.form.get('name')
        # Verificar que se haya proporcionado el nombre
        if not name:
            return jsonify({'error': 'El nombre del género es obligatorio'}), 400
        # Intentar agregar el género a través del repositorio
        genero = genero_repo.agregar_genero(name)
        # Redirigir al listado de géneros
        return redirect(url_for('genero_bp.obtener_generos'))
    except ValueError as e:
        # Si el género ya existe, manejar el error
         return redirect(url_for('error_page', error_message='Error al agregar el género: ' + str(e)))
    except Exception as e:
        # Manejo de cualquier otro error
        return redirect(url_for('error_page', error_message='Error al agregar el género: ' + str(e)))

@genero_bp.route('/generos/eliminar/<int:genero_id>', methods=['POST'])
def eliminar_genero(genero_id):
    try:
        # Intentar eliminar el género usando el repositorio
        genero_repo.eliminar_genero(genero_id)
        # Redirigir al listado de géneros
        return redirect(url_for('genero_bp.obtener_generos'))
    except ValueError as e:
        # Si el género no se encuentra
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        # Manejo de cualquier otro error
        return jsonify({'error': 'Error al eliminar el género', 'detalle': str(e)}), 500


@genero_bp.route('/generos/editar/<int:genero_id>', methods=['GET', 'POST'])
def editar_genero(genero_id):
    try:
        # Obtener el género por ID
        genero = genero_repo.obtener_genero_por_id(genero_id)
        if not genero:
            return jsonify({'error': 'Género no encontrado'}), 404
        # Si el método es POST, actualizar el género
        if request.method == 'POST':
            nuevo_nombre = request.form.get('name')
            if not nuevo_nombre:
                return jsonify({'error': 'El nombre del género es obligatorio'}), 400
            # Asignamos el nuevo nombre al género
            genero.name = nuevo_nombre
            # Intentamos actualizar el género
            genero_repo.actualizar_genero(genero)
            # Redirigir a la lista de géneros
            return redirect(url_for('genero_bp.obtener_generos'))
        # Si el método es GET, mostrar el formulario de edición con los datos actuales del género
        return render_template('generos/edit_generos.html', genero=genero)
    
    except ValueError as e:
        # Si el género ya existe o cualquier otro error de validación
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Error al editar el género', 'detalle': str(e)}), 500
