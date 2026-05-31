from db import DatabaseManager
from modelos import Proveedor, Cliente

class ContactoRepositorio:
    """
    Repositorio para manejar operaciones relacionadas con contactos en la base de datos.
    Args:
        db_config (dict): Configuración de la base de datos.
    """
    
    def __init__(self, db_config):
        self.db_config = db_config
      
    def obtener_proveedores(self) -> list[dict]:
        """ 
        Obtiene todos los proveedores de la base de datos.
        Returns:
            List[dict]: Una lista de diccionarios con los datos de cada proveedor.
        Raises:
            Error: Si hay un problema de conexión con la base de datos (heredado del DatabaseManager).
        """
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute("SELECT * FROM proveedores;")
            return cursor.fetchall()  # Retorna una lista de diccionarios con los datos de cada proveedor
                
                
    def agregar_proveedor(self, proveedor: Proveedor) -> None:
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

    def obtener_clientes(self) -> list[dict]:
        """
        Busca y obtiene todos los clientes de la base de datos.
        
        Returns:
            List[dict]: Una lista de diccionarios con los datos de cada cliente.

        Raises:
            Error: Si hay un problema de conexión con la base de datos (heredado del DatabaseManager).
        """
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute("SELECT * FROM clientes;")
            return cursor.fetchall()  # Retorna una lista de diccionarios con los datos de cada cliente

    def agregar_cliente(self, cliente: Cliente):    
        """
        Agrega un nuevo cliente a la base de datos.
        
        Args:
            cliente (Cliente): Una instancia de Cliente con los datos a insertar. El atributo 'id' se ignora.
            
        Raises:
            Error: Si hay un problema de conexión con la base de datos (heredado del DatabaseManager).
        """
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute(
                "INSERT INTO clientes (nombre, telefono, correo) VALUES (%s, %s, %s) ;",
                (cliente.nombre, cliente.telefono, cliente.correo) 
            )