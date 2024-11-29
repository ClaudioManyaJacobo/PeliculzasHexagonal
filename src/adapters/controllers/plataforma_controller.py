from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from src.adapters.repositories.plataforma_repository_sql import PlataformaRepositorySQL
from src.infrastructure.db import db
from src.domain.models.plataforma import Plataforma
import base64

plataforma_bp = Blueprint('plataforma_bp', __name__)
plataforma_repo = PlataformaRepositorySQL(db)

@plataforma_bp.route('/plataformas', methods=['GET'])
def obtener_plataformas():
    plataformas = db.session.query(Plataforma).all()
    for plataforma in plataformas:
        if plataforma.imagen:
            plataforma.imagen = base64.b64encode(plataforma.imagen).decode('utf-8')
    return render_template('plataformas/index.html', plataformas=plataformas)

@plataforma_bp.route('/plataformas/agregar', methods=['GET', 'POST'])
def agregar_plataforma():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        url_plataforma = request.form.get('url_plataforma')
        imagen = request.files.get('imagen')

        if imagen is None:
            return jsonify({'error': 'La imagen es requerida'}), 400
        
        try:
            # Lee los datos binarios de la imagen y la almacena
            imagen_binaria = imagen.read()
            plataforma = plataforma_repo.agregar_plataforma(nombre, url_plataforma, imagen_binaria)
            return redirect(url_for('plataforma_bp.obtener_plataformas'))
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
    return render_template('plataformas/add.html')

@plataforma_bp.route('/plataformas/editar/<int:id>', methods=['GET', 'POST'])
def editar_plataforma(id):
    plataforma = Plataforma.query.get(id)
    if not plataforma:
        return jsonify({'error': 'Plataforma no encontrada'}), 404

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        url_plataforma = request.form.get('url_plataforma')
        imagen = request.files.get('imagen')

        if imagen:
            imagen_binaria = imagen.read()
            try:
                plataforma = plataforma_repo.editar_plataforma(id, nombre, url_plataforma, imagen_binaria)
                return redirect(url_for('plataforma_bp.obtener_plataformas'))
            except ValueError as e:
                return jsonify({'error': str(e)}), 400
        else:
            try:
                plataforma = plataforma_repo.editar_plataforma(id, nombre, url_plataforma, None)
                return redirect(url_for('plataforma_bp.obtener_plataformas'))
            except ValueError as e:
                return jsonify({'error': str(e)}), 400
    return render_template('plataformas/edit.html', plataforma=plataforma)

@plataforma_bp.route('/plataformas/eliminar/<int:id>', methods=['GET'])
def eliminar_plataforma(id):
    try :
        plataforma = plataforma_repo.eliminar_plataforma(id)
        return redirect(url_for('plataforma_bp.obtener_plataformas'))
    except ValueError as e:
        return jsonify({'error': str(e)}), 400