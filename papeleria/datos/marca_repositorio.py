from db import DatabaseManager

class MarcaRepositorio:
    """
    Repositorio para manejar operaciones relacionadas con marcas en la base de datos.
    Args:
        db_config (dict): Configuración de la base de datos.
    """
    def __init__(self, db_config):
        self.db_config = db_config
        
    def obtener_todos(self) -> list[dict]:
        """
        Obtiene todas las marcas de la base de datos.
        Returns:
            List[dict]: Una lista de diccionarios con los datos de cada marca.
        Raises:
            Error: Si hay un problema de conexión con la base de datos (heredado del DatabaseManager).
        """
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute("SELECT * FROM marcas")
            return cursor.fetchall() # Retorna una lista de diccionarios con los datos de cada marca

    def agregar(self, nombre) -> int:
        """
        Agrega una nueva marca a la base de datos.
        Args:
            nombre (str): El nombre de la marca a agregar.
        Raises:
            Error: Si hay un problema de conexión con la base de datos (heredado del DatabaseManager).
        """
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute("INSERT INTO marcas (nombre_marca) VALUES (%s)", (nombre,))
            return cursor.lastrowid  # Retornar el ID generado