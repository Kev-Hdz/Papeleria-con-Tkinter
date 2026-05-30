
from db import DatabaseManager
from modelos import Cliente


"""
Controlador del acceso a la base de datos de la tabla clientes
"""
class ClienteRepositorio:
    def __init__(self, db_config):
        self.db_config = db_config

    def obtener_clientes(self):
        """Obtiene todos los clientes de la base de datos."""
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute("SELECT * FROM clientes;")
            filas = cursor.fetchall()
            
            return [Cliente(
                id=fila['id_cliente'], 
                nombre=fila['nombre'], 
                telefono=fila['telefono'], 
                correo=fila['correo']
                ) for fila in filas]
    
    def obtener_cliente(self, id: int):
        """Obtiene el cliente con el ID especificado."""
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute("SELECT * FROM clientes WHERE id_cliente = %s ;", (id))
            fila = cursor.fetchone()
            
            if fila:
                return Cliente(
                    id=fila['id_cliente'], 
                    nombre=fila['nombre'], 
                    telefono=fila['telefono'], 
                    correo=fila['correo']
                    )
            
        return None

    def agregar_cliente(self, cliente: Cliente):
        """Agrega un nuevo cliente a la base de datos."""
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute(
                "INSERT INTO clientes (nombre, telefono, correo) VALUES (%s, %s, %s) ;",
                (cliente.nombre, cliente.telefono, cliente.correo) 
            )