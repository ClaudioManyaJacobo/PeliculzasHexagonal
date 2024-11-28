from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from src.adapters.repositories.actor_repository_sql import ActorRepositorySQL
from src.domain.models.actor import Actor
from src.infrastructure.db import db
import base64

actor_bp = Blueprint('actor_bp', __name__)
actor_repo = ActorRepositorySQL(db)

@actor_bp.route('/actores', methods=['GET'])
def obtener_actores():
    # Obtén la lista de actores desde la base de datos
    actores = db.session.query(Actor).all()
    # Procesa la imagen si existe
    for actor in actores:
        if actor.imagen:
            # Codifica la imagen en Base64 si está presente
            actor.imagen = base64.b64encode(actor.imagen).decode('utf-8')
    # Pasa los actores al template
    return render_template('actores/index_actores.html', actores=actores)

@actor_bp.route('/actores/agregar', methods=['GET', 'POST'])
def agregar_actor():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        url_actor = request.form.get('url_actor')
        imagen = request.files.get('imagen')
        
        if imagen:
            imagen_binaria = imagen.read()  # Leemos la imagen y la convertimos en binario
            try:
                # Agregamos el actor al repositorio y lo guardamos en la variable actor
                actor = actor_repo.agregar_actor(nombre, url_actor, imagen_binaria)
                return redirect(url_for('actor_bp.obtener_actores'))
            except ValueError as e:
                return jsonify({'error': str(e)}), 400
        else:
            return jsonify({'error': 'La imagen es requerida'}), 400

    return render_template('actores/add_actores.html')


@actor_bp.route('/actores/editar/<int:id>', methods=['GET', 'POST'])
def editar_actor(id):
    actor = Actor.query.get(id)
    if not actor:
        return jsonify({'error': 'Actor no encontrado'}), 404
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        url_actor = request.form.get('url_actor')
        imagen = request.files.get('imagen')

        if imagen:
            imagen_binaria = imagen.read()  # Leemos la imagen y la convertimos en binario
            try:
                # Llamamos al método de edición del repositorio
                actor = actor_repo.editar_actor(id, nombre, url_actor, imagen_binaria)
                return redirect(url_for('actor_bp.obtener_actores'))
            except ValueError as e:
                return jsonify({'error': str(e)}), 400
        else:
            try:
                # Llamamos al método de edición sin imagen si no se proporciona una
                actor = actor_repo.editar_actor(id, nombre, url_actor, None)
                return redirect(url_for('actor_bp.obtener_actores'))
            except ValueError as e:
                return jsonify({'error': str(e)}), 400

    return render_template('actores/edit_actores.html', actor=actor)


@actor_bp.route('/actores/eliminar/<int:id>', methods=['GET'])
def eliminar_actor(id):
    try:
        # Llama al método de eliminación en el repositorio
        actor = actor_repo.eliminar_actor(id)
        return redirect(url_for('actor_bp.obtener_actores'))
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

