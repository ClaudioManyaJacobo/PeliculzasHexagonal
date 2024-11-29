# src/domain/models/pelicula.py
from src.infrastructure.db import db
from src.domain.models.pelicula_genero import PeliculaGenero
from src.domain.models.pelicula_actor import PeliculaActor
from src.domain.models.pelicula_plataforma import PeliculaPlataforma
class Pelicula(db.Model):
    __tablename__ = 'peliculas'  

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    duracion = db.Column(db.Integer, nullable=False)
    sinopsis = db.Column(db.String(500), nullable=False)
    anio = db.Column(db.Integer, nullable=False)
    director = db.Column(db.String(100), nullable=False)
    url_video = db.Column(db.String(100), nullable=False)
    generos = db.relationship('Genero', secondary='pelicula_genero', back_populates='peliculas')
    actores = db.relationship('Actor', secondary='pelicula_actor', back_populates='peliculas')
    plataformas = db.relationship('Plataforma', secondary='pelicula_plataforma', back_populates='peliculas')
    imagen = db.Column(db.LargeBinary, nullable=True)

    def __init__(self, nombre, duracion, sinopsis, anio, director, url_video, imagen=None):
        self.nombre = nombre
        self.duracion = duracion
        self.sinopsis = sinopsis
        self.anio = anio
        self.director = director
        self.url_video = url_video
        self.imagen = imagen 

    def __repr__(self):
        return f"<Pelicula {self.nombre}>"