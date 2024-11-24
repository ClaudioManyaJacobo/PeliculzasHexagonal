# src/adapters/repositories/pelicula_repository_sql.py
from src.domain.models.pelicula import Pelicula
from sqlalchemy.sql import text

class PeliculaRepositorySQL:
    def __init__(self, db):
        self.db = db

    #    Dentro del método obtener_todas_las_peliculas
    def obtener_todas_las_peliculas(self):
    # Usa text() para la consulta SQL
        peliculas_query = self.db.session.execute(text('SELECT id, nombre, duracion, sinopsis, anio, director FROM peliculas'))
        return peliculas_query.fetchall()

    def agregar_pelicula(self, nombre, duracion, sinopsis, anio, director):
        # Aquí va la lógica para agregar una nueva película
        pelicula = Pelicula(nombre, duracion, sinopsis, anio, director)
        self.db.session.add(pelicula)
        self.db.session.commit()
        return pelicula
