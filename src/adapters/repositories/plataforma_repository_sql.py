from sqlalchemy.sql import text
from src.domain.models.plataforma import Plataforma

class PlataformaRepositorySQL:
    def __init__(self, db):
        # Inicializa el repositorio con la instancia de la base de datos
        self.db = db

    # Método para obtener todas las plataformas de la base de datos
    def obtener_todas_las_plataformas(self):
        # Ejecuta una consulta SQL directa para obtener las plataformas
        plataforma_query = self.db.session.execute(text('SELECT id, nombre, url_plataforma FROM plataformas'))
        # Devuelve todos los resultados de la consulta
        return plataforma_query.fetchall()

    def obtener_plataforma_por_id(self, plataforma_id):
        return Plataforma.query.get(plataforma_id)
    
    def agregar_plataforma(self, nombre, url_plataforma, imagen):
        platafroma_existente = Plataforma.query.filter_by(nombre=nombre).first()
        if platafroma_existente:
            raise ValueError(f"La plataforma '{nombre}' ya existe en la base de datos.")
        
        plataforma = Plataforma(nombre, url_plataforma, imagen)
        self.db.session.add(plataforma)
        self.db.session.commit()
        return plataforma
    
    def editar_plataforma(self, id, nombre, url_plataforma, imagen):
        plataforma = Plataforma.query.get(id)
        if not plataforma:
            raise ValueError(f"La plataforma con ID '{id}' no se encuentra en la base de datos.")
        
        plataforma.nombre = nombre
        plataforma.url_plataforma = url_plataforma
        plataforma.imagen = imagen if imagen else plataforma.imagen

        self.db.session.commit()
        return plataforma
    
    def eliminar_plataforma(self, id):
        plataforma = Plataforma.query.get(id)
        if not plataforma:
            raise ValueError(f"Plataforma con ID {id} no encontrada.")
        self.db.session.delete(plataforma)
        self.db.session.commit()
        return plataforma

