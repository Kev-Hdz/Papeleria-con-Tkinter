from datetime import datetime
from modelos import Cliente
from modelos import DetalleVenta

class Venta:
    """
    Representa una venta realizada en la papelería.
    
    Args:
        id (int): Identificador único de la venta.
        fecha_venta (datetime): Fecha de la venta.
        cliente (Cliente): Objeto Cliente asociado a la venta (puede ser None para ventas sin cliente registrado).
        detalles (list): Lista de objetos DetalleVenta que componen la venta.
        total (float): Total de la venta calculado a partir de los detalles.
    
    """

    def __init__(self, fecha_venta: datetime, cliente: Cliente = None, id: int | None = None):
        self.id = id
        self.fecha_venta = fecha_venta
        self.cliente = cliente              # objeto Cliente o None
        self.detalles = []                  # lista de DetalleVenta
        self.total = 0.0

    def agregar_detalle(self, detalle: DetalleVenta):
        """Agrega un DetalleVenta y recalcula el total."""
        self.detalles.append(detalle)
        self.calcular_total()

    def calcular_total(self):
        """Calcula el total sumando todos los subtotales de los detalles."""
        self.total = sum(d.subtotal for d in self.detalles)
        return self.total

    def __str__(self):
        return f"Venta #{self.id} - ${self.total:.2f}"
