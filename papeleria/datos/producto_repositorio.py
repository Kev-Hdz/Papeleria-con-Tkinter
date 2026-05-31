from db import DatabaseManager
from modelos import  ProductoPapeleria

class ProductoRepositorio:
    """Repositorio para manejar operaciones relacionadas con productos en la base de datos.
    Args:
        db_config (dict): Configuración de la base de datos.
    """
    
    def __init__(self, db_config):
        self.db_config = db_config
      
    def obtener_todos(self) -> list[dict]:
        """ 
        Obtiene todos los productos de la base de datos.
        Returns:
            List[dict]: Una lista de diccionarios con los datos de cada producto.
        Raises:
            Error: Si hay un problema de conexión con la base de datos (heredado del DatabaseManager).
        """
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute("SELECT * FROM productos;")
            return cursor.fetchall()  # Retorna una lista de diccionarios con los datos de cada producto
                
                
    def agregar(self, producto: ProductoPapeleria) -> None:
        """
        Agrega un nuevo producto a la base de datos.
        Args:
            producto (ProductoPapeleria): El producto a agregar.
        Raises:
            Error: Si hay un problema de conexión con la base de datos (heredado del DatabaseManager).
        """
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute(
                "INSERT INTO productos (nombre, id_categoria, id_marca, descripcion, precio_compra, precio_venta, existencia, id_proveedor, fecha_registro) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ;",
                (producto.nombre, producto.id_categoria, producto.id_marca, producto.descripcion,
                 producto._precio_compra, producto._precio_venta, producto._existencia,
                 producto.id_proveedor, producto.fecha_registro)
            )
    def actualizar(self, id: int, producto: ProductoPapeleria) -> None:
        """
        Actualiza un producto existente en la base de datos.
        Args:
            id (int): El ID del producto a actualizar.
            producto (ProductoPapeleria): El producto con los nuevos datos.
        Raises:
            Error: Si hay un problema de conexión con la base de datos (heredado del DatabaseManager).
        """
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute(
                "UPDATE productos SET nombre = %s, id_categoria = %s, id_marca = %s, descripcion = %s, precio_compra = %s, precio_venta = %s, existencia = %s, id_proveedor = %s, fecha_registro = %s WHERE id = %s;",
                (producto.nombre, producto.id_categoria, producto.id_marca, producto.descripcion,
                 producto._precio_compra, producto._precio_venta, producto._existencia,
                 producto.id_proveedor, producto.fecha_registro, id)
            )
            
    def eliminar(self, id: int) -> None:
        """
        Elimina un producto de la base de datos.
        Args:
            id (int): El ID del producto a eliminar.
        Raises:
            Error: Si hay un problema de conexión con la base de datos (heredado del DatabaseManager).
        """
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute("DELETE FROM productos WHERE id = %s;", (id,))
    
    def buscar(self, filtros: dict):
        """
        Busca productos en la base de datos según los filtros proporcionados.
        Args:
            filtros (dict): Un diccionario con los campos y valores a filtrar (ejemplo: {"nombre": "cuaderno", "id_categoria": 2}).
        Returns:
            List[dict]: Una lista de diccionarios con los datos de los productos que coinciden con los filtros.
        Raises:
            Error: Si hay un problema de conexión con la base de datos (heredado del DatabaseManager).
        """
        with DatabaseManager(self.db_config) as cursor:
            query = "SELECT * FROM productos WHERE "
            conditions = []
            values = []
            for campo, valor in filtros.items():
                if campo == "nombre":
                    conditions.append(f"{campo} ILIKE %s")
                    values.append(f"%{valor}%")  # Búsqueda parcial para el nombre
                elif campo in ["id_categoria", "id_marca", "id_proveedor"]:
                    conditions.append(f"{campo} = %s")
                    values.append(valor)
                elif campo == "fecha_registro":
                    conditions.append(f"{campo}::date = %s")
                    values.append(valor)
            if not conditions:
                return []  # Retorna una lista vacía si no se proporcionan filtros válidos
            query += " AND ".join(conditions) + ";"
            cursor.execute(query, tuple(values))
            return cursor.fetchall()
    
    def buscar_por_id(self, id: int) -> dict | None:
        """
        Busca un producto en la base de datos por su ID.
        Args:
            id (int): El ID del producto a buscar.
        Returns:
            dict | None: Un diccionario con los datos del producto si se encuentra, o None si no se encuentra.
        Raises:
            Error: Si hay un problema de conexión con la base de datos (heredado del DatabaseManager).
        """
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute("SELECT * FROM productos WHERE id = %s;", (id,))
            resultado = cursor.fetchone()
            return ProductoPapeleria(**resultado) if resultado else None