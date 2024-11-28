# src/adapters/repositories/genero_repository_sql.py
from src.domain.models.genero import Genero
from sqlalchemy.sql import text

class GeneroRepositorySQL:
    def __init__(self, db):
        # Inicializa el repositorio con la instancia de la base de datos
        self.db = db

    # Método para obtener todos los géneros de la base de datos
    def obtener_todos_los_generos(self):
        # Ejecuta una consulta SQL directa para obtener los géneros
        generos_query = self.db.session.execute(text('SELECT id, name FROM generos'))
        # Devuelve todos los resultados de la consulta
        return generos_query.fetchall()

    # Método para agregar un nuevo género a la base de datos
    def agregar_genero(self, name):
        # Verifica si el género ya existe en la base de datos por su nombre
        genero_existente = Genero.query.filter_by(name=name).first()

        if genero_existente:
            # Lanza un error si el género ya existe
            raise ValueError(f"El género '{name}' ya existe en la base de datos.")

        # Si el género no existe, crea y agrega el nuevo género
        genero = Genero(name)
        self.db.session.add(genero)
        self.db.session.commit()  # Confirma la adición en la base de datos
        return genero
    
    # Método para obtener un género específico por su ID
    def obtener_genero_por_id(self, genero_id):
        # Utiliza query.get para obtener el género por su ID
        return Genero.query.get(genero_id)
    
    # Método para eliminar un género de la base de datos por su ID
    def eliminar_genero(self, genero_id):
        # Obtiene el género a eliminar por ID
        genero = self.obtener_genero_por_id(genero_id)
        
        if genero:
            # Elimina el género de la sesión y confirma la eliminación
            self.db.session.delete(genero)
            self.db.session.commit()
        else:
            # Lanza un error si el género no se encuentra en la base de datos
            raise ValueError("Género no encontrado")

    # Método para actualizar un género existente
    def actualizar_genero(self, genero):
        # Verifica si ya existe un género con el mismo nombre pero diferente ID
        genero_existente = Genero.query.filter(Genero.name == genero.name, Genero.id != genero.id).first()

        if genero_existente:
            # Lanza un error si el nuevo nombre ya está en uso
            raise ValueError(f"El género '{genero.name}' ya existe en la base de datos.")

        # Si el nombre es único, guarda los cambios en la base de datos
        self.db.session.commit()
