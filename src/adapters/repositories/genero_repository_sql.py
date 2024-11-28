from src.domain.models.genero import Genero
from sqlalchemy.sql import text

class GeneroRepositorySQL:
    def __init__(self, db):
        self.db = db

    def obtener_todos_los_generos(self):
        generos_query = self.db.session.execute(text('SELECT id, name FROM generos'))
        return generos_query.fetchall()

    def agregar_genero(self, name):
        # Verificar si el género ya existe
        genero_existente = Genero.query.filter_by(name=name).first()

        if genero_existente:
            raise ValueError(f"El género '{name}' ya existe en la base de datos.")

        # Si el género no existe, crear y agregar el nuevo género
        genero = Genero(name)
        self.db.session.add(genero)
        self.db.session.commit()
        return genero
    
    def obtener_genero_por_id(self, genero_id):
        return Genero.query.get(genero_id)
    
    def eliminar_genero(self, genero_id):
        # Obtener el género a eliminar por ID
        genero = self.obtener_genero_por_id(genero_id)
        
        if genero:
            self.db.session.delete(genero)
            self.db.session.commit()  # Confirmar eliminación en la base de datos
        else:
            raise ValueError("Género no encontrado")

    def actualizar_genero(self, genero):
        # Verificar si el nuevo nombre del género ya existe
        genero_existente = Genero.query.filter(Genero.name == genero.name, Genero.id != genero.id).first()

        if genero_existente:
            raise ValueError(f"El género '{genero.name}' ya existe en la base de datos.")

        # Si no existe, actualizar el género
        self.db.session.commit()
