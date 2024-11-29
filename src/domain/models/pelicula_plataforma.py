from src.infrastructure.db import db

class PeliculaPlataforma(db.Model):
    __tablename__ = 'pelicula_plataforma'

    pelicula_id = db.Column(db.Integer, db.ForeignKey('peliculas.id', ondelete="CASCADE"), primary_key=True)
    plataforma_id = db.Column(db.Integer, db.ForeignKey('plataformas.id', ondelete="CASCADE"), primary_key=True)
