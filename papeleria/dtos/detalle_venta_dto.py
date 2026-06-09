from datetime import datetime
from dataclasses import dataclass

@dataclass
class DetalleVentaDTO:
    id_detalle: int = None
    id_venta: int = None
    id_producto: int = None
    nombre_producto: str = ""
    cantidad: int = None
    precio_unitario: float = 0.0
    subtotal: float = 0.0