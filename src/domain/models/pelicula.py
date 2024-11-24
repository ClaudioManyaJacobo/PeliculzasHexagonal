# src/domain/models/pelicula.py
from src.infrastructure.db import db
from src.domain.models.pelicula_genero import PeliculaGenero

class Pelicula(db.Model):
    __tablename__ = 'peliculas'  # Nombre de la tabla en la base de datos

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    duracion = db.Column(db.Integer, nullable=False)
    # Recien agregados
    sinopsis = db.Column(db.String(500), nullable=False)
    anio = db.Column(db.Integer, nullable=False)
    director = db.Column(db.String(100), nullable=False)

    generos = db.relationship('Genero', secondary='pelicula_genero', back_populates='peliculas')


    def __init__(self, nombre, duracion, sinopsis, anio, director):
        self.nombre = nombre
        self.duracion = duracion
        # Recien agregados
        self.sinopsis = sinopsis
        self.anio = anio
        self.director = director

    def __repr__(self):
        return f"<Pelicula {self.nombre}>"
