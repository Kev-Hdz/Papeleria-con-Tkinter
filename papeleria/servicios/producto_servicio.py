from datos import ProductoRepositorio
from modelos import ProductoPapeleria

class ProductoServicio:
    def __init__(self, producto_repositorio: ProductoRepositorio):
        self.repositorio = producto_repositorio
        
    
    def agregar_producto(self, datos_producto: dict):
        """
        Agrega un nuevo producto a la base de datos.
        
        Args:
            datos_producto (dict): Un diccionario con los datos del producto a agregar. Las claves deben coincidir con los atributos de ProductoPapeleria, excepto 'id' que se ignora.
        Raises:
            Error: Si hay un problema de conexión con la base de datos (heredado del DatabaseManager).
        """
        producto = ProductoPapeleria(**datos_producto)
        self.repositorio.agregar(producto)
    def actualizar_producto(self, id: int, datos_actualizados: dict):
        """
        Actualiza los datos de un producto existente en la base de datos.
        
        Args:
            id (int): El ID del producto a actualizar.
            datos_actualizados (dict): Un diccionario con los datos actualizados del producto. Las claves deben coincidir con los atributos de ProductoPapeleria, excepto 'id' que se ignora.
        Raises:
            Error: Si hay un problema de conexión con la base de datos (heredado del DatabaseManager).
        """
        producto = ProductoPapeleria(id=id, **datos_actualizados)
        self.repositorio.actualizar(producto)
    
    def eliminar_producto(self, id: int):
        """
        Elimina un producto de la base de datos.
        
        Args:
            id (int): El ID del producto a eliminar.
        Raises:
            Error: Si hay un problema de conexión con la base de datos (heredado del DatabaseManager).
        """
        
        self.repositorio.eliminar(id)
        
    def consultar_productos(self) -> list:
        """
        Obtiene todos los productos disponibles en la base de datos.
        
        Returns:
            list: Una lista de instancias de ProductoPapeleria con los datos de cada producto.
            Retorna una lista vacía si no se encuentran productos en la tabla.

        Raises:
            Error: Si hay un problema de conexión con la base de datos (heredado del DatabaseManager).
        """
        return self.repositorio.obtener_todos()
    
    def buscar_producto(self, filtros: dict) -> list:
        """
        Busca productos basados en los filtros proporcionados.
        
        Args:
            filtros (dict): Un diccionario con los criterios de búsqueda. Las claves pueden ser:
            'nombre', 
            'id_categoria', 
            'id_marca', 
            'id_proveedor',
            'fecha_registro', 


        Returns:
            list: Una lista de instancias de ProductoPapeleria que coinciden con los filtros.
            Retorna una lista vacía si no se encuentran productos que coincidan.

        Raises:
            Error: Si hay un problema de conexión con la base de datos (heredado del DatabaseManager).
        """
        filtros_limpios = {k: v for k, v in filtros.items() if v}
        if not filtros_limpios:
            return self.consultar_productos()
            
        return self.repositorio.buscar(filtros_limpios)