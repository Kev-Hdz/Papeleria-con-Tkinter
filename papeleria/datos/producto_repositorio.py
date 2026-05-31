from db import DatabaseManager
from modelos import  Categoria, Marca, Proveedor, ProductoPapeleria

class ProductoRepositorio:
    """Repositorio para manejar operaciones relacionadas con productos en la base de datos.
    Args:
        db_config (dict): Configuración de la base de datos.
    """
    # Centralizamos la consulta base para no repetirla
    _BASE_QUERY = """
        SELECT 
            p.id_producto, 
            p.nombre AS nombre_producto, 
            p.descripcion AS descripcion_producto,
            p.precio_compra, 
            p.precio_venta, 
            p.existencia, 
            p.fecha_registro,
            c.id_categoria, 
            c.nombre_categoria,
            m.id_marca, 
            m.nombre_marca,
            pr.id_proveedor,
            pr.nombre AS nombre_proveedor,
            pr.telefono AS telefono_proveedor,
            pr.correo AS correo_proveedor,
            pr.direccion AS direccion_proveedor 
        FROM productos p
        INNER JOIN categorias c ON p.id_categoria = c.id_categoria
        LEFT JOIN  marcas m ON p.id_marca = m.id_marca
        LEFT JOIN  proveedores pr ON p.id_proveedor = pr.id_proveedor
    """

    def __init__(self, db_config):
        self.db_config = db_config

    def _mapear_producto(self, fila: dict) -> ProductoPapeleria:
        """
        Método privado para centralizar la lógica de mapeo de la base de datos al Dominio.
        Args:
            fila (dict): Un diccionario con los datos de la consulta.
        """
        return ProductoPapeleria(
            id=fila['id_producto'],
            nombre=fila['nombre_producto'],
            categoria=Categoria(id=fila['id_categoria'], nombre=fila['nombre_categoria']),
            
            # Se reincorpora la validación de nulos según el script de BD
            marca=Marca(id=fila['id_marca'], nombre=fila['nombre_marca']) if fila['id_marca'] else None,
            
            descripcion=fila['descripcion_producto'],
            precio_compra=fila['precio_compra'],
            precio_venta=fila['precio_venta'],
            existencia=fila['existencia'],
            
            # Se reincorpora la validación de nulos según el script de BD
            proveedor=Proveedor(
                id=fila['id_proveedor'], 
                nombre=fila['nombre_proveedor'], 
                telefono=fila['telefono_proveedor'], 
                correo=fila['correo_proveedor'], 
                direccion=fila['direccion_proveedor']
            ) if fila['id_proveedor'] else None,
            
            fecha_registro=fila['fecha_registro']
        )
      
    def obtener_todos(self):
        """
        Obtiene todos los productos de la base de datos.
        Returns:
            List[ProductoPapeleria]: Una lista de objetos ProductoPapeleria.
        Raises:
            Error: Si hay un problema de conexión con la base de datos (heredado del DatabaseManager).
        """ 
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute(self._BASE_QUERY)
            # Usamos el helper para mapear cada fila
            return [self._mapear_producto(fila) for fila in cursor.fetchall()]
    
    def obtener_por_id(self, id: int):
        """
        Obtiene un producto por su ID. 
        Args:
            id (int): El ID del producto a obtener.
        Returns:
            ProductoPapeleria: El objeto ProductoPapeleria si se encuentra, None en caso contrario.
        Raises:
            Error: Si hay un problema de conexión con la base de datos (heredado del DatabaseManager).
        """
        query = self._BASE_QUERY + " WHERE p.id_producto = %s;"
        
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute(query, (id,))
            fila = cursor.fetchone()
            
            if fila:
                return self._mapear_producto(fila)
            return None

    def agregar(self, producto: ProductoPapeleria):
        """
        Agrega un nuevo producto a la base de datos.
        Args:
            producto (ProductoPapeleria): El producto a agregar.
        Raises:
            Error: Si hay un problema de conexión con la base de datos (heredado del DatabaseManager).
        """
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute(
                "INSERT INTO productos (nombre, id_categoria, id_marca, descripcion, precio_compra, precio_venta, existencia, id_proveedor, fecha_registro) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);",
                (
                    producto.nombre, 
                    producto.categoria.id, 
                    producto.marca.id if producto.marca else None, 
                    producto.descripcion, 
                    producto.precio_compra, 
                    producto.precio_venta, 
                    producto.existencia, 
                    producto.proveedor.id if producto.proveedor else None, 
                    producto.fecha_registro
                ) 
            )