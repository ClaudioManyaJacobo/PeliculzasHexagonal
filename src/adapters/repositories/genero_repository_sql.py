from src.domain.models.genero import Genero
from sqlalchemy.sql import text

class GeneroRepositorySQL:
    def __init__(self, db):
        self.db = db

    def obtener_todos_los_generos(self):
        generos_query = self.db.session.execute(text('SELECT id, name FROM generos'))
        return generos_query.fetchall()

    def agregar_genero(self, name):
        genero = Genero(name)
        self.db.session.add(genero)
        self.db.session.commit()
        return genero
