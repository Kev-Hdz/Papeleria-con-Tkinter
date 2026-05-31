from db import DatabaseManager
from modelos import Proveedor

class ProveedorRepositorio:
    """
    Repositorio para manejar operaciones relacionadas con proveedores en la base de datos.
    Args:
        db_config (dict): Configuración de la base de datos.
    """
    
    def __init__(self, db_config):
        self.db_config = db_config
      
    def obtener_todos(self):
        """ 
        Obtiene todos los proveedores de la base de datos.
        Returns:
            List[Proveedor]: Una lista de objetos Proveedor.
        Raises:
            Error: Si hay un problema de conexión con la base de datos (heredado del DatabaseManager).
        """
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute("SELECT * FROM proveedores;")
            filas = cursor.fetchall()
            return [Proveedor(
                id=fila['id_proveedor'],
                nombre=fila['nombre'],
                telefono=fila['telefono'],
                correo=fila['correo'],
                direccion=fila['direccion']
            ) for fila in filas]
                
    def obtener_por_id(self, id: int):
        """
        Obtiene un proveedor por su ID.
        Args:
            id (int): El ID del proveedor a obtener.
        Returns:
            Proveedor: El objeto Proveedor si se encuentra, None en caso contrario.
        Raises:
            Error: Si hay un problema de conexión con la base de datos (heredado delDatabaseManager).
        """
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute("SELECT * FROM proveedores WHERE id_proveedor = %s ;", (id,))
            fila = cursor.fetchone()
            if fila:
                return Proveedor(
                    id=fila['id_proveedor'],
                    nombre=fila['nombre'],
                    telefono=fila['telefono'],
                    correo=fila['correo'],
                    direccion=fila['direccion']
                )
            return None
                
    def agregar(self, proveedor: Proveedor):
        """
        Agrega un nuevo proveedor a la base de datos.
        Args:
            proveedor (Proveedor): El proveedor a agregar.
        Raises:
            Error: Si hay un problema de conexión con la base de datos (heredado del DatabaseManager).
        """
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute(
                "INSERT INTO proveedores (nombre, telefono, correo, direccion) VALUES (%s, %s, %s, %s) ;",
                (proveedor.nombre, proveedor.telefono, proveedor.correo, proveedor.direccion) 
            )
        