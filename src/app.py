from flask import Flask, flash, jsonify, redirect, render_template, request, send_from_directory, url_for
from sqlalchemy.sql import text
from src.infrastructure.db import db

from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from src.adapters.controllers.auth_controller import auth_bp  # Importa el blueprint de autenticación
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

from src.adapters.controllers.pelicula_controller import pelicula_bp
from src.adapters.controllers.genero_controller import genero_bp
from src.adapters.controllers.actor_controller import actor_bp
from src.adapters.controllers.plataforma_controller import plataforma_bp


import os
# Inicializa la aplicación Flask
app = Flask(__name__)


# Configuración de la base de datos para SQL Server
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://sa:SQLserver123456@localhost:1433/Peliculizate?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa la base de datos con la app
db.init_app(app)
bcrypt = Bcrypt(app)

# Configuración de Flask-Login 
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

def load_user(user_id):
    # Aquí debes cargar al usuario de la base de datos usando su ID
    return User.query.get(int(user_id))  # Se asume que el ID del usuario es un entero




class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)


class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@ app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


## Aqui termina el cambio











# Registra el blueprint
app.register_blueprint(pelicula_bp)
app.register_blueprint(genero_bp)
app.register_blueprint(actor_bp)
app.register_blueprint(plataforma_bp)
app.register_blueprint(auth_bp, url_prefix='/auth')  # Registra el blueprint de autenticación

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
