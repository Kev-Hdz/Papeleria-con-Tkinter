
from db import DatabaseManager
from modelos import Cliente



class ClienteRepositorio:
    """
    Controlador de persistencia para la entidad Cliente.
    
    Se encarga de abstraer las consultas SQL y devolver objetos de dominio, aislando 
    la base de datos de la lógica de negocio.
    """
    def __init__(self, db_config):
        self.db_config = db_config

    def obtener_todos(self) -> list[Cliente]:
        """
        Busca y obtiene todos los clientes de la base de datos.
        
        Returns:
            list[Cliente]: Una lista de instancias de Cliente con los datos de cada cliente.
            Retorna una lista vacía si no se encuentran clientes en la tabla.

        Raises:
            Error: Si hay un problema de conexión con la base de datos (heredado del DatabaseManager).
        """
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute("SELECT * FROM clientes;")
            filas = cursor.fetchall()
            
            return [Cliente(
                id=fila['id_cliente'], 
                nombre=fila['nombre'], 
                telefono=fila['telefono'], 
                correo=fila['correo']
                ) for fila in filas]
    
    def obtener_por_id(self, id: int) -> Cliente | None:
        """
        Busca y obtiene un cliente específico basado en su identificador único.

        Args:
            id (int): El número de identificación primario del cliente en la base de datos.

        Returns:
            Cliente | None: Una instancia instanciada con los datos del cliente si se encuentra.
            Retorna None si el identificador no existe en la tabla.

        Raises:
            Error: Si hay un problema de conexión con la base de datos (heredado del DatabaseManager).
        """
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute("SELECT * FROM clientes WHERE id_cliente = %s ;", (id,))
            fila = cursor.fetchone()
            
            if fila:
                return Cliente(
                    id=fila['id_cliente'], 
                    nombre=fila['nombre'], 
                    telefono=fila['telefono'], 
                    correo=fila['correo']
                    )
            
        return None

    def agregar(self, cliente: Cliente):    
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