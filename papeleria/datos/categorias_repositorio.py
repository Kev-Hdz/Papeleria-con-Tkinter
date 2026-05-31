from db import DatabaseManager
from modelos import Categoria

class CategoriaRepositorio:
    """
    Repositorio para manejar operaciones relacionadas con categorías en la base de datos.
    Args:        db_config (dict): Configuración de la base de datos.
    """
    def __init__(self, db_config):
        self.db_config = db_config
        
    def obtener_todos(self):
        """
        Obtiene todas las categorías de la base de datos.
        Returns:
            List[Categoria]: Una lista de objetos Categoria.
        Raises:
            Error: Si hay un problema de conexión con la base de datos (heredado del DatabaseManager).
        """
        
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute("SELECT * FROM categorias ORDER BY id_categoria ASC")
            filas = cursor.fetchall()
            return [Categoria(id=fila['id_categoria'], nombre=fila['nombre_categoria']) for fila in filas]

    def obtener_por_id(self, id: int):
        """
        Obtiene una categoría por su ID.
        Args:
            id (int): El ID de la categoría a obtener.
        Returns:
            Categoria: El objeto Categoria si se encuentra, None en caso contrario.
        Raises:
            Error: Si hay un problema de conexión con la base de datos (heredado del DatabaseManager).
        """
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute("SELECT * FROM categorias WHERE id_categoria = %s", (id,))
            fila = cursor.fetchone()
            if fila:
                return Categoria(id=fila['id_categoria'], nombre=fila['nombre_categoria'])
            return None
        
    def agregar(self, categoria: Categoria):
        """
        Agrega una nueva categoría a la base de datos.
        Args:
            categoria (Categoria): El objeto Categoria a agregar. El atributo 'id' se ignora ya que es auto-incremental.
        Raises:
            Error: Si hay un problema de conexión con la base de datos (heredado del DatabaseManager).
        """
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute("INSERT INTO categorias (nombre_categoria) VALUES (%s)", (categoria.nombre,))
            categoria.id = cursor.lastrowid  # Asignar el ID generado al objeto Categoria  
    