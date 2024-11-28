from src.infrastructure.db import db

class PeliculaActor(db.Model):
    __tablename__ = 'pelicula_actor'

    pelicula_id = db.Column(db.Integer, db.ForeignKey('peliculas.id', ondelete="CASCADE"), primary_key=True)
    actor_id = db.Column(db.Integer, db.ForeignKey('actores.id', ondelete="CASCADE"), primary_key=True)
