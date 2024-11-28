from flask import Flask, jsonify, render_template, request
from flask import Flask, jsonify
from sqlalchemy.sql import text
from src.infrastructure.db import db
from src.adapters.controllers.pelicula_controller import pelicula_bp
from src.adapters.controllers.genero_controller import genero_bp

# Inicializa la aplicación Flask
app = Flask(__name__)

# Configuración de la base de datos para SQL Server
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://sa:Teamoariel0112@GINOS/Bonita?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa la base de datos con la app
db.init_app(app)

# Registra el blueprint
app.register_blueprint(pelicula_bp)
app.register_blueprint(genero_bp)

with app.app_context():
    db.create_all()
    print("Tablas creadas si no existían.")

# Manejo de errores generales
@app.errorhandler(500)
def internal_error(error):
    """ Redirige a la página de error general cuando ocurre un error 500. """
    return render_template('error.html', error_message='Ocurrió un error inesperado, por favor intente nuevamente más tarde.'), 500

@app.errorhandler(404)
def page_not_found(error):
    """ Redirige a la página de error general cuando ocurre un error 404. """
    return render_template('error.html', error_message='Página no encontrada.'), 404

# Ruta de prueba para verificar la conexión a la base de datos
@app.route('/')
def conexion_exitosa():
    """
    Verifica la conexión a la base de datos con una consulta SQL básica.
    """
    try:
        # Verifica la conexión a la base de datos
        with app.app_context():
            db.session.execute(text('SELECT 1'))  # Consulta simple para verificar conexión
        return jsonify({"mensaje": "Conexión a la base de datos exitosa"}), 200
    except Exception as e:
        return jsonify({"error": "Error al conectar con la base de datos", "detalle": str(e)}), 500

@app.route('/error')
def error_page():
    error_message = request.args.get('error_message', 'Ocurrió un error inesperado.')
    return render_template('error.html', error_message=error_message)

# Inicia la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True)
