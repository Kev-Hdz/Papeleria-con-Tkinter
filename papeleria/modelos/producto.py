
from datetime import datetime

from modelos import Categoria
from modelos import Proveedor
from modelos import Marca


class ProductoPapeleria:
    """
    Representa un artículo que se vende en la papelería.
    
    Args:
        id (int): Identificador único del producto.
        nombre (str): Nombre del producto.
        categoria (Categoria): Objeto Categoria al que pertenece el producto.
        marca (Marca): Objeto Marca a la que pertenece el producto.
        descripcion (str): Descripción del producto.
        precio_compra (float): Precio de compra del producto.
        precio_venta (float): Precio de venta del producto.
        existencia (int): Cantidad disponible del producto.
        proveedor (Proveedor): Objeto Proveedor que suministra el producto.
        fecha_registro (datetime): Fecha de registro del producto.
    
    Raises:
        ValueError: Si los precios son negativos o si la existencia es negativa.
    """

    def __init__(self, id: int, nombre: str, categoria: Categoria, marca: Marca, descripcion: str,
                 precio_compra: float, precio_venta: float, existencia: int, proveedor: Proveedor, fecha_registro: datetime):
        
        if precio_compra < 0 or precio_venta < 0:
            raise ValueError("Los precios no pueden ser negativos.")
        if existencia < 0:
            raise ValueError("La existencia no puede ser negativa.")

        self.id = id
        self.nombre = nombre
        self.categoria = categoria          # objeto Categoria
        self.marca = marca
        self.descripcion = descripcion
        
        self._precio_compra = float(precio_compra)
        self._precio_venta = float(precio_venta)
        self._existencia = int(existencia)
        
        self.proveedor = proveedor          # objeto Proveedor
        self.fecha_registro = fecha_registro
        
    def registrar_venta(self, cantidad: int) -> None:
        """
        Registra una venta del producto, actualizando la existencia.
        
        Args:
            cantidad (int): Cantidad vendida.
        
        Raises:
            ValueError: Si la cantidad vendida es menor o igual a cero o si no hay suficiente existencia.
        """
        if cantidad <= 0:
            raise ValueError("La cantidad vendida debe ser mayor a cero.")
        if cantidad > self._existencia:
            raise ValueError("No hay suficiente existencia para realizar la venta.")
        
        self._existencia -= cantidad
        
