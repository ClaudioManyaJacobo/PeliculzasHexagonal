from src.infrastructure.db import db
from src.domain.models.pelicula import Pelicula  # Importa el modelo Pelicula
from src.domain.models.pelicula_genero import PeliculaGenero

class Genero(db.Model):
    __tablename__ = 'generos'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    # Relación de muchos a muchos con Pelicula usando la tabla intermedia 'pelicula_genero'
    peliculas = db.relationship('Pelicula', secondary='pelicula_genero', back_populates='generos')

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"<Genero {self.name}>"