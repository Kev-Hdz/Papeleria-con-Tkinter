from db import DatabaseManager
from modelos import Marca

class MarcaRepositorio:
    """
    Repositorio para manejar operaciones relacionadas con marcas en la base de datos.
    Args:
        db_config (dict): Configuración de la base de datos.
    """
    def __init__(self, db_config):
        self.db_config = db_config
        
    def obtener_todos(self):
        """
        Obtiene todas las marcas de la base de datos.
        Returns:
            List[Marca]: Una lista de objetos Marca.
        Raises:
            Error: Si hay un problema de conexión con la base de datos (heredado del DatabaseManager).
        """
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute("SELECT * FROM marcas")
            filas = cursor.fetchall()
            return [Marca(id=fila['id_marca'], nombre=fila['nombre_marca']) for fila in filas]

    def obtener_por_id(self, id: int):
        """
        Obtiene una marca por su ID.
        Args:
            id (int): El ID de la marca a obtener.
        Returns:
            Marca: El objeto Marca si se encuentra, None en caso contrario.
        Raises:
            Error: Si hay un problema de conexión con la base de datos (heredado del DatabaseManager).
        """
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute("SELECT * FROM marcas WHERE id_marca = %s", (id,))
            fila = cursor.fetchone()
            if fila:
                return Marca(id=fila['id_marca'], nombre=fila['nombre_marca'])
            return None
    