from flask import Flask, jsonify
from sqlalchemy.sql import text
from src.infrastructure.db import db
from src.adapters.controllers.pelicula_controller import pelicula_bp  # Importa el blueprint

# Inicializa la aplicación Flask
app = Flask(__name__)

# Configuración de la base de datos para SQL Server
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://sa:Teamoariel0112@GINOS/Bonita?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa la base de datos con la app
db.init_app(app)

# Registra el blueprint
app.register_blueprint(pelicula_bp)

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

# Inicia la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True)
