from db import DatabaseManager
from modelos import Producto

class ProductoRepositorio:
    def __init__(self, db_config):
        self.db_config = db_config
      
    def obtener_productos(self):
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute("SELECT * FROM productos;")
            return cursor.fetchall
    
    def obtener_producto(self, id: int):
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute("SELECT * FROM productos WHERE id = %s ;", (id))
            return cursor.fetchone()
        
    def agregar_producto(self, producto: Producto):
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute(
                "INSERT INTO productos (nombre, id_categoria, id_marca, descripcion, precio_compra, precio_venta, existencia, id_proveedor, fecha_registro) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ;",
                (producto.nombre, producto.categoria.id, producto.marca.id, producto.descripcion, producto.precio_compra, producto.precio_venta, producto.existencia, producto.proveedor.id, producto.fecha_registro) 
            )