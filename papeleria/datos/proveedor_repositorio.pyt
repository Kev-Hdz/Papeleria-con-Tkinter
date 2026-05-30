from db import DatabaseManager
from modelos import Proveedor

class ProveedorRepositorio:
    def __init__(self, db_config):
        self.db_config = db_config
      
    def obtener_proveedores(self):
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute("SELECT * FROM proveedores;")
            return cursor.fetchall
    
    def obtener_proveedor(self, id: int):
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute("SELECT * FROM proveedores WHERE id = %s ;", (id))
            return cursor.fetchone()
        
    def agregar_proveedor(self, proveedor: Proveedor):
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute(
                "INSERT INTO proveedores (nombre, telefono, correo, direccion) VALUES (%s, %s, %s) ;",
                (proveedor.nombre, proveedor.telefono, proveedor.correo, proveedor.direccion) 
            )
        