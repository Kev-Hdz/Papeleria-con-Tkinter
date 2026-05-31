from datetime import datetime

class DetalleVenta:
    """
    Representa una línea de producto dentro de una venta.
    
    Args:
        producto_id (int): El ID del producto vendido.
        cantidad (int): La cantidad vendida.
        precio_unitario (float): El precio unitario al momento de la venta.
        subtotal (float): El subtotal calculado como cantidad * precio_unitario.

    """

    def __init__(self, producto_id: int, cantidad: int, precio_unitario: float, id: int | None = None):
        self.id = id
        self.producto_id = producto_id
        self.cantidad = int(cantidad)
        self.precio_unitario = float(precio_unitario)
        
    @property
    def subtotal(self):
        """
        Calcula el subtotal de este detalle de venta.
        
        Returns:
            float: El subtotal calculado como cantidad * precio_unitario.
        """
        return self.cantidad * self.precio_unitario