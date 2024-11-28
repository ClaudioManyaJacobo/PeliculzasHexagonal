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

        pelicula_existente = Pelicula.query.filter_by(nombre=nombre).first()
        if pelicula_existente:
            raise ValueError(f"Ya existe una película con el nombre '{nombre}'.")
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

    def obtener_pelicula_por_id(self, pelicula_id):
        return self.db.session.query(Pelicula).options(joinedload(Pelicula.generos)).filter_by(id=pelicula_id).first()

    def eliminar_pelicula(self, pelicula_id):
        # Obtener la película para eliminar
        pelicula = self.obtener_pelicula_por_id(pelicula_id)
        if pelicula:
            self.db.session.delete(pelicula)
        else:
            raise ValueError("Película no encontrada")

    def editar_pelicula(self, pelicula_id, nombre=None, duracion=None, sinopsis=None, anio=None, director=None, url_video=None, generos=None, imagen=None):
        pelicula = self.obtener_pelicula_por_id(pelicula_id)
        if not pelicula:
            raise ValueError("Película no encontrada")

        # Actualizamos solo los campos proporcionados
        if nombre:
            pelicula.nombre = nombre
        if duracion:
            pelicula.duracion = duracion
        if sinopsis:
            pelicula.sinopsis = sinopsis
        if anio:
            pelicula.anio = anio
        if director:
            pelicula.director = director
        if url_video:
            pelicula.url_video = url_video
        if imagen is not None:
            pelicula.imagen = imagen

        # Actualizamos los géneros si se proporcionan
        if generos is not None:
            pelicula.generos.clear()  # Eliminamos las relaciones existentes
            for genero_id in generos:
                genero = Genero.query.get(genero_id)
                if genero:
                    pelicula.generos.append(genero)

        # Guardamos los cambios
        self.db.session.commit()
        return pelicula