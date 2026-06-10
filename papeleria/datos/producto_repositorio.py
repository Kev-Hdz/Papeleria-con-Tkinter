from db.database_manager import DatabaseManager
from dtos import ProductoDTO
class ProductoRepositorio:

    def __init__(self, db_config: dict):
        self.db_config = db_config
        
        # Consulta base con JOINs para reutilizar en obtener_todos, buscar y buscar_por_id
        self._base_query = """
            SELECT 
                p.id_producto,
                p.nombre,
                p.id_categoria,
                c.nombre_categoria AS nombre_categoria,
                p.id_marca,
                m.nombre_marca AS nombre_marca,
                p.descripcion,
                p.precio_compra,
                p.precio_venta,
                p.existencia,
                p.id_proveedor,
                prov.nombre AS nombre_proveedor,
                p.fecha_registro
            FROM productos p
            LEFT JOIN categorias c ON p.id_categoria = c.id_categoria
            LEFT JOIN marcas m ON p.id_marca = m.id_marca
            LEFT JOIN proveedores prov ON p.id_proveedor = prov.id_proveedor
            WHERE p.fecha_eliminado IS NULL
        """
      
    def consultar(self) -> list[ProductoDTO]:
        """Consulta todos los productos detallados con sus relaciones.
        Returns:
            List[ProductoDTO]: Una lista de objetos ProductoDTO con los datos de cada producto y sus relaciones. Si no hay productos, devuelve una lista vacía.
        Raises:
            Error: Si hay un problema de conexión con la base de datos (heredado del DatabaseManager).
        """
        query = f"{self._base_query};"
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute(query)
            return [ProductoDTO(**row) for row in cursor.fetchall()]  
                
    def agregar(self, producto: ProductoDTO) -> None:
        """Agrega un nuevo producto a la base de datos.
        Args:
            producto (ProductoDTO): Un objeto ProductoDTO con los datos del producto a agregar. Se espera que el objeto ya haya pasado por las validaciones de sus propiedades.
        Raises:
            Error: Si hay un problema de conexión con la base de datos (heredado del DatabaseManager).
        """
        query = """
            INSERT INTO productos (
                nombre, id_categoria, id_marca, descripcion, 
                precio_compra, precio_venta, existencia, id_proveedor, fecha_registro
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute(
                query,
                (
                    producto.nombre, 
                    producto.id_categoria, 
                    producto.id_marca, 
                    producto.descripcion,
                    producto.precio_compra,  
                    producto.precio_venta,   
                    producto.existencia,    
                    producto.id_proveedor, 
                    producto.fecha_registro
                )
            )
            
    def actualizar(self, id_producto: int, producto: ProductoDTO) -> None:
        """Actualiza un producto existente en la base de datos.
        Args:
            id_producto (int): El ID del producto a actualizar.
            producto (ProductoDTO): Un objeto ProductoDTO con los datos actualizados del producto. Se espera que el objeto ya haya pasado por las validaciones de sus propiedades.
        Raises:
            ValueError: Si el producto con el ID especificado no existe.
            Error: Si hay un problema de conexión con la base de datos (heredado del DatabaseManager).
        """
        query = """
            UPDATE productos SET 
                nombre = %s, 
                id_categoria = %s, 
                id_marca = %s, 
                descripcion = %s, 
                precio_compra = %s, 
                precio_venta = %s, 
                existencia = %s, 
                id_proveedor = %s 
            WHERE id_producto = %s AND fecha_eliminado IS NULL;
        """
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute(
                query,
                (
                    producto.nombre, 
                    producto.id_categoria, 
                    producto.id_marca, 
                    producto.descripcion,
                    producto.precio_compra, 
                    producto.precio_venta, 
                    producto.existencia, 
                    producto.id_proveedor, 
                    id_producto
                )
            )
            
    def eliminar(self, id_producto: int) -> None:
        """Elimina físicamente un producto por su ID.
        Args:            
            id_producto (int): El ID del producto a eliminar.
        Raises:            
            Error: Si hay un problema de conexión con la base de datos (heredado del DatabaseManager).
        """
        query = "UPDATE productos SET fecha_eliminado = CURRENT_TIMESTAMP WHERE id_producto = %s AND fecha_eliminado IS NULL;"
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute(query, (id_producto,))
    
    def buscar(self, filtros: dict) -> list[ProductoDTO]:
        """Busca productos aplicando filtros dinámicos.
        Args:
            filtros (dict): Un diccionario con los campos a filtrar y sus valores. Ejemplo: {"nombre": "cuaderno", "id_categoria": 2}
        Returns:
            list[ProductoDTO]: Una lista de objetos ProductoDTO que cumplen con los filtros aplicados o una lista vacía si no se encuentran productos que coincidan.
        Raises:
            Error: Si hay un problema de conexión con la base de datos (heredado del DatabaseManager).
        """
        conditions = []
        values = []
        
        # Mapeo seguro de filtros entrantes a columnas de la base de datos
        for campo, valor in filtros.items():
            if campo == "nombre":
                conditions.append("p.nombre LIKE %s")
                values.append(f"%{valor}%")
            elif campo in ["id_categoria", "id_marca", "id_proveedor"]:
                conditions.append(f"p.{campo} = %s")
                values.append(valor)
            elif campo == "fecha_registro":
                conditions.append("DATE(p.fecha_registro) = %s")
                values.append(valor)
                
        if not conditions:
            return []
            
        query = f"{self._base_query} AND " + " AND ".join(conditions) + ";"
        
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute(query, tuple(values))
            return [ProductoDTO(**row) for row in cursor.fetchall()]

    def buscar_por_id(self, id_producto: int) -> ProductoDTO | None:
        """Busca un único producto por su ID. 
        Args:
            id_producto (int): El ID del producto a buscar.
        Returns:
            ProductoDTO | None: Un objeto ProductoDTO con los datos del producto encontrado, o None si no se encuentra ningún producto con ese ID.
        Raises:
            Error: Si hay un problema de conexión con la base de datos (heredado del DatabaseManager).
        """
        query = f"{self._base_query} AND p.id_producto = %s AND p.fecha_eliminado IS NULL;"
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute(query, (id_producto,))
            row = cursor.fetchone()
            return ProductoDTO(**row) if row else None
        
    def esta_activo(self, id_producto: int) -> bool:
        """Verifica si un producto está activo (no eliminado) por su ID.
        Args:
            id_producto (int): El ID del producto a verificar.
        Returns:
            bool: True si el producto está activo, False si no existe o está marcado como eliminado.
        Raises:
            Error: Si hay un problema de conexión con la base de datos (heredado del DatabaseManager).
        """
        query = "SELECT fecha_eliminado FROM productos WHERE id_producto = %s;"
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute(query, (id_producto,))
            row = cursor.fetchone()
            return row is not None and row["fecha_eliminado"] is None
        
    def obtener_categorias(self) -> list[dict]:
        """Obtiene el catálogo maestro de categorías
        
        Returns:
            List[dict]: Una lista de diccionarios con las categorías disponibles, cada diccionario contiene 'id_categoria' y 'nombre_categoria'. Si no hay categorías, devuelve una lista vacía.
        Raises:
            Error: Si hay un problema de conexión con la base de datos (heredado del DatabaseManager).
        """
        query = "SELECT id_categoria, nombre_categoria FROM categorias;"
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute(query)
            return cursor.fetchall()
        
    def obtener_marcas(self) -> list[dict]:
        """Obtiene el catálogo maestro de marcas.
        Returns:
            List[dict]: Una lista de diccionarios con las marcas disponibles, cada diccionario contiene 'id_marca' y 'nombre_marca'. Si no hay marcas, devuelve una lista vacía.
        Raises:
            Error: Si hay un problema de conexión con la base de datos (heredado del DatabaseManager).
        """
        query = "SELECT id_marca, nombre_marca FROM marcas;"
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute(query)
            return cursor.fetchall()