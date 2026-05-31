from datetime import datetime
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

    def __init__(self, fecha_venta: datetime, id_cliente: int = None, id: int | None = None):
        self.id = id
        self.fecha_venta = fecha_venta
        self.id_cliente = id_cliente              # ID del cliente o None
        self.detalles = []                  # lista de DetalleVenta
    
    def agregar_detalle(self, detalle: DetalleVenta):
        """
        Agrega un detalle de venta a la venta y actualiza el total.
        
        Args:
            detalle (DetalleVenta): Detalle de venta a agregar.
        """
        self.detalles.append(detalle)
  
    @property
    def total(self):
        """
        Calcula el total de la venta sumando el subtotal de cada detalle.
        
        Returns:
            float: Total de la venta.
        """
        return sum(detalle.subtotal for detalle in self.detalles)
        
    
    
    def validad_venta(self):
        """
        Confirma la venta, asegurándose de que tenga al menos un detalle y un total mayor a cero.
        
        Raises:
            ValueError: Si la venta no tiene detalles o el total es cero o negativo.
        """
        if not self.detalles:
            raise ValueError("La venta debe tener al menos un detalle.")
        if self.total <= 0:
            raise ValueError("El total de la venta debe ser mayor a cero.")
