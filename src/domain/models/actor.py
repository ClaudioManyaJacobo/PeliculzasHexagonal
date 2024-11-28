from src.infrastructure.db import db

class Actor(db.Model):
    __tablename__ = 'actores'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    url_actor = db.Column(db.String(100), nullable=False)
    imagen = db.Column(db.LargeBinary, nullable=True)

    peliculas = db.relationship('Pelicula', secondary='pelicula_actor', back_populates='actores')


    def __init__(self, nombre, url_actor, imagen=None):
        self.nombre = nombre
        self.url_actor = url_actor
        self.imagen = imagen

    def __repr__(self):
        return f"<{self.nombre}>"