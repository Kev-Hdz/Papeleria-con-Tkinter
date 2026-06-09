from datetime import datetime

from datos import ProductoRepositorio
from dtos import ProductoDTO
class ProductoServicio:
    """Capa de aplicación que coordina la lógica de negocio y la persistencia."""

    def __init__(self, producto_repositorio: ProductoRepositorio):
        self.repositorio = producto_repositorio
        
    def registrar_producto(self, producto: ProductoDTO) -> None:
        """Gestiona la creación de un nuevo producto a través del repositorio.
        Args:
            producto (ProductoDTO): Un objeto ProductoDTO con los datos del producto a registrar. 
        """
        if not producto.nombre:
            raise ValueError("El nombre del producto no puede estar vacío.")
        if producto.precio_venta <= 0:
            raise ValueError("El precio de venta debe ser mayor a cero.")
        if producto.existencia < 0:
            raise ValueError("La existencia no puede ser negativa.")
        producto.fecha_registro = producto.fecha_registro or datetime.now().strftime("%Y-%m-%d")
        self.repositorio.agregar(producto)
        
    def actualizar_producto(self, id_producto: int, producto_actualizado: ProductoDTO) -> None:
        """Gestiona la actualización del producto a través del repositorio.
        Args:
            id_producto (int): El ID del producto a actualizar.
            producto_actualizado (ProductoDTO): Un objeto ProductoDTO con los datos actualizados del producto. 
        """
        producto_existente = self.repositorio.buscar_por_id(id_producto)
        if not producto_existente:
            raise ValueError(f"No se encontró ningún producto con ID {id_producto}.")
        if not producto_actualizado.nombre:
            raise ValueError("El nombre del producto no puede estar vacío.")
        if producto_actualizado.precio_venta <= 0:
            raise ValueError("El precio de venta debe ser mayor a cero.")
        if producto_actualizado.existencia < 0:
            raise ValueError("La existencia no puede ser negativa.")
        self.repositorio.actualizar(id_producto, producto_actualizado)
    
    def eliminar_producto(self, id_producto: int) -> None:
        """Gestiona la eliminación del producto a través del repositorio.
        Args:
            id_producto (int): El ID del producto a eliminar.
        """
        producto_existente = self.repositorio.buscar_por_id(id_producto)
        if not producto_existente:
            raise ValueError(f"No se encontró ningún producto con ID {id_producto}.")

        self.repositorio.eliminar(id_producto)
        
    def consultar_productos(self) -> list[ProductoDTO]:
        """Consulta todos los productos disponibles a través del repositorio.
        Returns:
            List[ProductoDTO]: Una lista de objetos ProductoDTO con los datos de cada producto y sus relaciones. Si no hay productos, devuelve una lista vacía.
        """
        return self.repositorio.consultar()
    
    def buscar_producto(self, filtros: dict) -> list[ProductoDTO]:
        """Busca productos según criterios específicos y los retorna mapeados a objetos.
         Args:
             filtros (dict): Un diccionario con los criterios de búsqueda, por ejemplo {'nombre': 'cuaderno', 'id_categoria': 2}.
             - nombre: str
             - id_categoria: int
             - id_marca: int
             - id_proveedor: int
             - fecha_registro: str (en formato 'YYYY-MM-DD')
         Returns:
             List[ProductoDTO]: Una lista de objetos ProductoDTO que cumplen con los criterios de búsqueda. Si no se encuentra ningún producto, devuelve una lista vacía.
         """
        filtros_limpios = {k: v for k, v in filtros.items() if v}
        if not filtros_limpios:
            return self.consultar_productos()
            
        return self.repositorio.buscar(filtros_limpios)
    
    def consultar_categorias(self) -> list[dict]:
        """Devuelve las categorías disponibles (se mantiene como diccionarios para lectura simple).
        Returns:
            List[dict]: Una lista de diccionarios con las categorías disponibles, cada diccionario contiene 'id_categoria' y 'nombre_categoria'. Si no hay categorías, devuelve una lista vacía.
        """
        return self.repositorio.obtener_categorias()

    def consultar_marcas(self) -> list[dict]:
        """Devuelve las marcas disponibles.
        Returns:
            List[dict]: Una lista de diccionarios con las marcas disponibles, cada diccionario contiene 'id_marca' y 'nombre_marca'. Si no hay marcas, devuelve una lista vacía.
        """
        return self.repositorio.obtener_marcas()