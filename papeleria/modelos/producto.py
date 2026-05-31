"""
Modelo: ProductoPapeleria
Representa un artículo que se vende en la papelería.
"""


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
    """

    def __init__(self, id: int, nombre: str, categoria: Categoria, marca: Marca, descripcion: str,
                 precio_compra: float, precio_venta: float, existencia: int, proveedor: Proveedor, fecha_registro: datetime):
        self.id = id
        self.nombre = nombre
        self.categoria = categoria          # objeto Categoria
        self.marca = marca
        self.descripcion = descripcion
        self.precio_compra = float(precio_compra)
        self.precio_venta = float(precio_venta)
        self.existencia = int(existencia)
        self.proveedor = proveedor          # objeto Proveedor
        self.fecha_registro = fecha_registro

    def __str__(self):
        return self.nombre
