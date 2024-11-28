# src/adapters/repositories/actor_repository_sql.py
from sqlalchemy.sql import text
from src.domain.models.actor import Actor

class ActorRepositorySQL:
    def __init__(self, db):
        # Inicializa el repositorio con la instancia de la base de datos
        self.db = db

    # Método para obtener todos los actores de la base de datos
    def obtener_todos_los_actores(self):
        # Ejecuta una consulta SQL directa para obtener los actores
        actor_query = self.db.session.execute(text('SELECT id, nombre, url_actor FROM actores'))
        # Devuelve todos los resultados de la consulta
        return actor_query.fetchall()

    # Método para obtener un actor específico por su ID
    def obtener_actor_por_id(self, actor_id):
        # Utiliza query.get para obtener el actor por su ID
        return Actor.query.get(actor_id)

    # Método para agregar un nuevo actor a la base de datos
    def agregar_actor(self, nombre, url_actor, imagen):
        # Verifica si el actor ya existe en la base de datos por su nombre
        actor_existente = Actor.query.filter_by(nombre=nombre).first()

        if actor_existente:
            # Lanza un error si el actor ya existe
            raise ValueError(f"El actor '{nombre}' ya existe en la base de datos.")

        # Si el actor no existe, crea y agrega el nuevo actor
        actor = Actor(nombre, url_actor, imagen)
        self.db.session.add(actor)
        self.db.session.commit()  # Confirma la adición en la base de datos
        return actor  # Devuelve el objeto Actor recién creado

    # Método para editar un actor existente en la base de datos
    def editar_actor(self, id, nombre, url_actor, imagen):
        # Busca el actor por su ID
        actor = Actor.query.get(id)
        if not actor:
            # Lanza un error si el actor no se encuentra en la base de datos
            raise ValueError(f"El actor con ID '{id}' no se encuentra en la base de datos.")

        # Actualiza los atributos del actor con los nuevos valores proporcionados
        actor.nombre = nombre
        actor.url_actor = url_actor
        # Solo actualiza la imagen si se proporciona un nuevo valor
        actor.imagen = imagen if imagen else actor.imagen

        # Guarda los cambios en la base de datos
        self.db.session.commit()
        return actor  # Devuelve el actor actualizado

    # Método para eliminar un actor de la base de datos por su ID
    def eliminar_actor(self, id):
        # Busca el actor por su ID
        actor = Actor.query.get(id)
        if not actor:
            # Lanza un error si el actor no se encuentra en la base de datos
            raise ValueError(f"Actor con ID {id} no encontrado.")
        
        # Elimina el actor de la sesión y confirma la eliminación
        self.db.session.delete(actor)
        self.db.session.commit()
        return actor  # Devuelve el actor que fue eliminado
