from flask import Flask, jsonify, render_template, request, send_from_directory
from sqlalchemy.sql import text
from src.infrastructure.db import db
from src.adapters.controllers.pelicula_controller import pelicula_bp
from src.adapters.controllers.genero_controller import genero_bp
from src.adapters.controllers.actor_controller import actor_bp
from src.adapters.controllers.plataforma_controller import plataforma_bp
import os
# Inicializa la aplicación Flask
app = Flask(__name__)

# Configuración de la base de datos para SQL Server
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://sa:Teamoariel0112@GINOS/Peliculizate?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa la base de datos con la app
db.init_app(app)

# Registra el blueprint
app.register_blueprint(pelicula_bp)
app.register_blueprint(genero_bp)
app.register_blueprint(actor_bp)
app.register_blueprint(plataforma_bp)

with app.app_context():
    db.create_all()
    print("Tablas creadas si no existían.")

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

# Método para manejar errores y redirigir a la página error.html
@app.route('/error')
def error_page():
    error_message = request.args.get('error_message', 'Ocurrió un error inesperado.')
    return render_template('error.html', error_message=error_message)

# Manejador de errores global para capturar excepciones no tratadas
@app.errorhandler(Exception)
def handle_exception(e):
    # Manejo de errores personalizados en español
    if isinstance(e, ValueError):
        error_message = "Error de valor: Asegúrese de que los datos ingresados sean correctos."
    elif isinstance(e, KeyError):
        error_message = "Error de clave: Falta un dato importante en la solicitud."
    elif isinstance(e, FileNotFoundError):
        error_message = "Archivo no encontrado: Verifique que el archivo exista y sea accesible."
    elif isinstance(e, ZeroDivisionError):
        error_message = "Error de división por cero: No se puede dividir un número por cero."
    elif isinstance(e, TypeError):
        error_message = "Error de tipo: Hay un problema con los tipos de datos utilizados."
    elif hasattr(e, 'code') and e.code == 404:
        error_message = "Error 404: La página solicitada no fue encontrada."
    else:
        # Para otras excepciones no específicas, mostrar un mensaje general en español
        error_message = "Ocurrió un error inesperado. Por favor, intente de nuevo más tarde."

    # Redirige al usuario a la página de error con un mensaje en español
    return render_template('error.html', error_message=error_message), 500

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

# Inicia la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True)
