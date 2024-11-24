# src/domain/models/pelicula_genero.py
from src.infrastructure.db import db

class PeliculaGenero(db.Model):
    __tablename__ = 'pelicula_genero'

    pelicula_id = db.Column(db.Integer, db.ForeignKey('peliculas.id', ondelete="CASCADE"), primary_key=True)
    genero_id = db.Column(db.Integer, db.ForeignKey('generos.id', ondelete="CASCADE"), primary_key=True)
