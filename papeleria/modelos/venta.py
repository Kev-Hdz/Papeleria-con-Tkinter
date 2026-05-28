"""
Modelo: Venta y DetalleVenta
Representa una venta realizada y cada línea de producto dentro de ella.
"""


class DetalleVenta:
    """Representa una línea de producto dentro de una venta."""

    def __init__(self, producto, cantidad, precio_unitario):
        self.producto = producto            # objeto ProductoPapeleria
        self.cantidad = int(cantidad)
        self.precio_unitario = float(precio_unitario)
        self.subtotal = self.calcular_subtotal()

    def calcular_subtotal(self):
        """Calcula el subtotal multiplicando cantidad por precio unitario."""
        return self.cantidad * self.precio_unitario


class Venta:
    """Representa una venta realizada en la papelería."""

    def __init__(self, id_venta, fecha_venta, cliente=None):
        self.id_venta = id_venta
        self.fecha_venta = fecha_venta
        self.cliente = cliente              # objeto Cliente o None
        self.detalles = []                  # lista de DetalleVenta
        self.total = 0.0

    def agregar_detalle(self, detalle):
        """Agrega un DetalleVenta y recalcula el total."""
        self.detalles.append(detalle)
        self.calcular_total()

    def calcular_total(self):
        """Calcula el total sumando todos los subtotales de los detalles."""
        self.total = sum(d.subtotal for d in self.detalles)
        return self.total

    def __str__(self):
        return f"Venta #{self.id_venta} - ${self.total:.2f}"
