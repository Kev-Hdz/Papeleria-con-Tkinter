from db import DatabaseManager

class CategoriaRepositorio:
    """
    Repositorio para manejar operaciones relacionadas con categorías en la base de datos.
    Args:        db_config (dict): Configuración de la base de datos.
    """
    def __init__(self, db_config):
        self.db_config = db_config
        
    def obtener_todos(self) -> list[dict]:
        """
        Obtiene todas las categorías de la base de datos.
        Returns:
            List[dict]: Una lista de diccionarios con los datos de cada categoría.
        Raises:
            Error: Si hay un problema de conexión con la base de datos (heredado del DatabaseManager).
        """
        
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute("SELECT * FROM categorias ORDER BY id_categoria ASC")
            return cursor.fetchall()  # Retorna una lista de diccionarios con los datos de cada categoría

    def agregar(self, nombre) -> int:
        """
        Agrega una nueva categoría a la base de datos.
        Args:
            nombre (str): El nombre de la categoría a agregar.
        Returns:
            int: El ID de la categoría recién agregada.
        Raises:
            Error: Si hay un problema de conexión con la base de datos (heredado del DatabaseManager).
        """
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute("INSERT INTO categorias (nombre_categoria) VALUES (%s)", (nombre,))
            return cursor.lastrowid  # Retornar el ID generado