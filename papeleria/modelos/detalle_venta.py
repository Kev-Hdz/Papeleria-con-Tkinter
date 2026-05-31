from datetime import datetime
from modelos import ProductoPapeleria

class DetalleVenta:
    """
    Representa una línea de producto dentro de una venta.
    
    Args:
        producto (ProductoPapeleria): El producto vendido.
        cantidad (int): La cantidad vendida.
        precio_unitario (float): El precio unitario al momento de la venta.
        subtotal (float): El subtotal calculado como cantidad * precio_unitario.
    
    """

    def __init__(self, producto: ProductoPapeleria, cantidad: int, precio_unitario: float, id: int | None = None):
        self.id = id
        self.producto = producto            # objeto ProductoPapeleria
        self.cantidad = int(cantidad)
        self.precio_unitario = float(precio_unitario)
        self.subtotal = self.calcular_subtotal()

    def calcular_subtotal(self):
        """Calcula el subtotal multiplicando cantidad por precio unitario."""
        return self.cantidad * self.precio_unitario