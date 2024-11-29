# src/adapters/repositories/pelicula_repository_sql.py
from src.domain.models.pelicula import Pelicula
from src.domain.models.genero import Genero
from src.domain.models.actor import Actor
from src.domain.models.plataforma import Plataforma
from sqlalchemy.sql import text
from sqlalchemy.orm import joinedload

class PeliculaRepositorySQL:
    def __init__(self, db):
        # Inicializa el repositorio con la instancia de la base de datos
        self.db = db

    # Método para obtener todas las películas de la base de datos
    def obtener_todas_las_peliculas(self):
        # Se asegura de cargar los géneros asociados a cada película utilizando joinedload
        peliculas = self.db.session.query(Pelicula).options(joinedload(Pelicula.generos)).all()
        return peliculas

    # Método para agregar una nueva película a la base de datos
    def agregar_pelicula(self, nombre, duracion, sinopsis, anio, director, url_video, generos, imagen, actores, plataformas):
        # Verifica si ya existe una película con el mismo nombre
        pelicula_existente = Pelicula.query.filter_by(nombre=nombre).first()
        if pelicula_existente:
            raise ValueError(f"Ya existe una película con el nombre '{nombre}'.")

        # Crea una nueva instancia de la película
        pelicula = Pelicula(
            nombre=nombre, 
            duracion=duracion, 
            sinopsis=sinopsis, 
            anio=anio, 
            director=director, 
            url_video=url_video,
            imagen=imagen
        )

        # Asocia los géneros seleccionados con la película
        for genero_id in generos:
            genero = Genero.query.get(genero_id)  # Obtiene el género por su ID
            if genero:
                pelicula.generos.append(genero)  # Agrega el género a la lista de géneros de la película
        
        # Asocia los actores seleccionados con la película
        for actor_id in actores:
            actor = Actor.query.get(actor_id)
            if actor:
                pelicula.actores.append(actor)
        
        for plataforma_id in plataformas:
            plataforma = Plataforma.query.get(plataforma_id)
            if plataforma:
                pelicula.plataformas.append(plataforma)

        # Agrega la nueva película a la sesión y la guarda en la base de datos
        self.db.session.add(pelicula)
        self.db.session.commit()
        
        return pelicula

    # Método para obtener una película específica por su ID
    def obtener_pelicula_por_id(self, pelicula_id):
        # Carga la película junto con sus géneros usando joinedload para evitar consultas adicionales
        return self.db.session.query(Pelicula).options(joinedload(Pelicula.generos)).filter_by(id=pelicula_id).first()

    # Método para eliminar una película de la base de datos
    def eliminar_pelicula(self, pelicula_id):
        # Obtiene la película a eliminar
        pelicula = self.obtener_pelicula_por_id(pelicula_id)
        if pelicula:
            # Elimina la película de la base de datos
            self.db.session.delete(pelicula)
        else:
            # Lanza un error si la película no se encuentra
            raise ValueError("Película no encontrada")

    # Método para editar los detalles de una película existente
    def editar_pelicula(self, pelicula_id, nombre=None, duracion=None, sinopsis=None, anio=None, director=None, url_video=None, generos=None, imagen=None, actores=None, plataformas=None):
        # Obtiene la película a editar por su ID
        pelicula = self.obtener_pelicula_por_id(pelicula_id)
        if not pelicula:
            raise ValueError("Película no encontrada")

        # Actualiza solo los campos proporcionados
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

        # Actualiza los géneros si se proporciona una lista de géneros
        if generos is not None:
            pelicula.generos.clear()  # Elimina las relaciones actuales de géneros
            for genero_id in generos:
                genero = Genero.query.get(genero_id)
                if genero:
                    pelicula.generos.append(genero)
        
        # Actualiza los actores si se proporciona una lista de actores
        if actores is not None:
            pelicula.actores.clear()  # Elimina las relaciones actuales de actores
            for actor_id in actores:
                actor = Actor.query.get(actor_id)
                if actor:
                    pelicula.actores.append(actor)

        if plataformas is not None:
            pelicula.plataformas.clear()
            for plataforma_id in plataformas:
                plataforma = Plataforma.query.get(plataforma_id)
                if plataforma:
                    pelicula.plataformas.append(plataforma)

        # Guarda los cambios realizados en la base de datos
        self.db.session.commit()
        return pelicula
