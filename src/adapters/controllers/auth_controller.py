# from flask import Blueprint, render_template, request, redirect, url_for, flash
# from flask_login import login_user, login_required, logout_user
# from flask_bcrypt import Bcrypt
# from src.domain.models.user import LoginForm
# from src.adapters.repositories.user_repository_sql import UserRepositorySQL

# # Crea el blueprint para las rutas de autenticación
# auth_bp = Blueprint('auth', __name__)

# bcrypt = Bcrypt()

# # Ruta para el login
# @auth_bp.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         # Llamar al repositorio para obtener el usuario
#         user = UserRepositorySQL.get_user_by_username(form.username.data)
#         if user:
#             if bcrypt.check_password_hash(user.password, form.password.data):
#                 login_user(user)
#                 return redirect(url_for('dashboard'))  # Redirigir a la página de dashboard o la que sea
#         flash('Invalid username or password')
#     return render_template('login.html', form=form)
