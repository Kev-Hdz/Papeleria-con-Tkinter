from datetime import datetime
from dataclasses import dataclass

from dtos import DetalleVentaDTO

@dataclass
class VentaDTO:
    id_venta: int = None
    fecha_venta: datetime = None
    detalles: list[DetalleVentaDTO] = None
    id_cliente: int = None
    nombre_cliente: str = ""
    total: float = 0.0

