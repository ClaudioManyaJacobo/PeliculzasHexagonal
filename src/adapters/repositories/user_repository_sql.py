# # src/adapters/repositories/user_repository_sql.py
# from src.domain.models.user import User
# from src.infrastructure.db import db

# class UserRepositorySQL:
#     @staticmethod
#     def get_user_by_username(username):
#         return User.query.filter_by(username=username).first()

#     @staticmethod
#     def add_user(user):
#         db.session.add(user)
#         db.session.commit()
