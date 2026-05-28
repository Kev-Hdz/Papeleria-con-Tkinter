"""
Modelo: ProductoPapeleria
Representa un artículo que se vende en la papelería.
"""


class ProductoPapeleria:
    """Representa un artículo que se vende en la papelería."""

    def __init__(self, id_producto, nombre, categoria, marca, descripcion,
                 precio_compra, precio_venta, existencia, proveedor, fecha_registro):
        self.id_producto = id_producto
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
