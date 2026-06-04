from db import DatabaseManager
from dtos import ProveedorDTO, ClienteDTO
class ContactoRepositorio:
    """
    Repositorio para manejar operaciones relacionadas con contactos en la base de datos.
    Args:
        db_config (dict): Configuración de la base de datos.
    """
    
    def __init__(self, db_config):
        self.db_config = db_config
      
    def consultar_proveedores(self) -> list[ProveedorDTO]:
        """ 
        Consulta todos los proveedores de la base de datos.
        Returns:
            List[ProveedorDTO]: Una lista de objetos ProveedorDTO. Si no se encuentra ningún proveedor, retorna una lista vacía.
        Raises:
            Error: Si hay un problema de conexión con la base de datos (heredado del DatabaseManager).
        """
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute("SELECT * FROM proveedores;")
            return [ProveedorDTO(**row) for row in cursor.fetchall()] 

    def registrar_proveedor(self, proveedor: ProveedorDTO) -> None:
        """
        Registra un nuevo proveedor en la base de datos.
        Args:
            proveedor (ProveedorDTO): El proveedor a registrar.
        Raises:
            Error: Si hay un problema de conexión con la base de datos (heredado del DatabaseManager).
        """
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute(
                "INSERT INTO proveedores (nombre, telefono, correo, direccion) VALUES (%s, %s, %s, %s) ;",
                (proveedor.nombre, proveedor.telefono, proveedor.correo, proveedor.direccion) 
            )

    def consultar_clientes(self) -> list[ClienteDTO]:
        """
        Consulta todos los clientes de la base de datos.
        Returns:
            List[ClienteDTO]: Una lista de objetos ClienteDTO. Si no se encuentra ningún cliente, retorna una lista vacía.
        Raises:
            Error: Si hay un problema de conexión con la base de datos (heredado del DatabaseManager).
        """
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute("SELECT * FROM clientes;")
            return [ClienteDTO(**row) for row in cursor.fetchall()]  # Retorna una lista de objetos ClienteDTO

    def registrar_cliente(self, cliente: ClienteDTO) -> None:    
        """
        Registra un nuevo cliente en la base de datos.
        Args:
            cliente (ClienteDTO): Una instancia de ClienteDTO con los datos a insertar. El atributo 'id' se ignora.
        Raises:
            Error: Si hay un problema de conexión con la base de datos (heredado del DatabaseManager).
        """
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute(
                "INSERT INTO clientes (nombre, telefono, correo) VALUES (%s, %s, %s) ;",
                (cliente.nombre, cliente.telefono, cliente.correo) 
            )
    
    def buscar_proveedor(self, filtro):
        """Busca un proveedor en la base de datos según los criterios especificados en el filtro.
        Args:
            filtro (dict): Un diccionario con las claves como nombres de columnas y los valores como los valores a buscar. 
        Returns:
            List[ProveedorDTO]: Una lista de objetos ProveedorDTO que coinciden con los criterios de búsqueda. Si no se encuentra ningún proveedor, retorna una lista vacía.
        Raises:
            Error: Si hay un problema de conexión con la base de datos (heredado del DatabaseManager).
        """
        # 1. Prevenir error si el filtro está vacío
        if not filtro:
            return []
        
        # 2. Validar que las claves sean columnas reales para evitar SQL Injection
        columnas_validas = ["nombre", "telefono", "correo", "direccion"] # Pon aquí tus columnas
        for clave in filtro.keys():
            if clave not in columnas_validas:
                raise ValueError(f"Intento de búsqueda con columna inválida: {clave}")

        # 3. Construir la consulta
        condiciones = []
        valores = []
        
        for clave, valor in filtro.items():
            condiciones.append(f"{clave} LIKE %s") 
            valores.append(valor)
            
        where_clause = " AND ".join(condiciones)
        query = f"SELECT * FROM proveedores WHERE {where_clause};"
        
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute(query, valores)
            return [ProveedorDTO(**row) for row in cursor.fetchall()] 

    
    def buscar_cliente(self, filtro: dict) -> list[ClienteDTO]:
        """Busca un cliente en la base de datos según los criterios especificados en el filtro.
        Args:
            filtro (dict): Un diccionario con las claves como nombres de columnas y los valores como los valores a buscar. 
            Ejemplo: {"nombre": "Cliente A", "telefono": "987654321"}  Filtros: nombre, telefono, correo
        Returns:
            List[ClienteDTO]: Una lista de objetos ClienteDTO que coinciden con los criterios de búsqueda. Si no se encuentra ningún cliente, retorna una lista vacía.
        Raises:
            Error: Si hay un problema de conexión con la base de datos (heredado del DatabaseManager).
        """
        if not filtro:
            return []
        
        columnas_validas = ["nombre", "telefono", "correo"] 
        for clave in filtro.keys():
            if clave not in columnas_validas:
                raise ValueError(f"Intento de búsqueda con columna inválida: {clave}")
            
        condiciones = []
        valores = []
        
        for clave, valor in filtro.items():
            condiciones.append(f"{clave} LIKE %s") 
            valores.append(valor)
            
        where_clause = " AND ".join(condiciones)
        query = f"SELECT * FROM clientes WHERE {where_clause};"
        
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute(query, valores)
            return [ClienteDTO(**row) for row in cursor.fetchall()]
    
    def consultar_proveedor_por_id(self, id_proveedor: int) -> ProveedorDTO | None:
        """Consulta un proveedor por su ID.
        Args:
            id_proveedor (int): El ID del proveedor a consultar.
        Returns:
            ProveedorDTO | None: Un objeto ProveedorDTO con los datos del proveedor encontrado. Si no se encuentra ningún proveedor con ese ID, retorna None.
        Raises:
            Error: Si hay un problema de conexión con la base de datos (heredado del DatabaseManager).
        """
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute("SELECT * FROM proveedores WHERE id_proveedor = %s;", (id_proveedor,))
            row = cursor.fetchone()
            return ProveedorDTO(**row) if row else None

    def consultar_cliente_por_id(self, id_cliente: int) -> ClienteDTO | None:
        """Consulta un cliente por su ID.
        Args:            
            id_cliente (int): El ID del cliente a consultar.
        Returns:            
            ClienteDTO | None: Un objeto ClienteDTO con los datos del cliente encontrado. Si no se encuentra ningún cliente con ese ID, retorna None.
        Raises:            
            Error: Si hay un problema de conexión con la base de datos (heredado del DatabaseManager).
        """
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute("SELECT * FROM clientes WHERE id_cliente = %s;", (id_cliente,))
            row = cursor.fetchone()
            return ClienteDTO(**row) if row else None