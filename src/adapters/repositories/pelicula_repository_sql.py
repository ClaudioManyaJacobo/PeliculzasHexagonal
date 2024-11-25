# src/adapters/repositories/pelicula_repository_sql.py
from src.domain.models.pelicula import Pelicula
from src.domain.models.genero import Genero
from sqlalchemy.sql import text
from sqlalchemy.orm import joinedload

class PeliculaRepositorySQL:
    def __init__(self, db):
        self.db = db

    #    Dentro del método obtener_todas_las_peliculas
    def obtener_todas_las_peliculas(self):
        # Asegúrate de cargar los géneros asociados
        peliculas = self.db.session.query(Pelicula).options(joinedload(Pelicula.generos)).all()
        return peliculas

    def agregar_pelicula(self, nombre, duracion, sinopsis, anio, director, url_video, generos, imagen):
        # Crear una nueva película
        pelicula = Pelicula(
            nombre=nombre, 
            duracion=duracion, 
            sinopsis=sinopsis, 
            anio=anio, 
            director=director, 
            url_video=url_video,
            imagen=imagen
        )

        # Obtener los géneros seleccionados por el id y asociarlos con la película
        for genero_id in generos:
            genero = Genero.query.get(genero_id)  # Obtener el género por ID
            if genero:
                pelicula.generos.append(genero)  # Asociar el género a la película

        # Guardar la película y los géneros asociados
        self.db.session.add(pelicula)
        self.db.session.commit()
        
        return pelicula
