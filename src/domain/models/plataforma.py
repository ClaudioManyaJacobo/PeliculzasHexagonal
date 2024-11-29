from src.infrastructure.db import db

class Plataforma(db.Model):
    __tablename__ = 'plataformas'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    url_plataforma = db.Column(db.String(100), nullable=False)
    imagen = db.Column(db.LargeBinary, nullable=True)

    peliculas = db.relationship('Pelicula', secondary='pelicula_plataforma', back_populates='plataformas')


    def __init__(self, nombre, url_plataforma, imagen=None):
        self.nombre = nombre
        self.url_plataforma = url_plataforma
        self.imagen = imagen

    def __repr__(self):
        return f"<{self.nombre}>"
    
