from datetime import datetime
from dataclasses import dataclass

@dataclass
class ProductoDTO:
    id_producto: int = None  # Se asignará automáticamente al insertar en la base de datos
    nombre: str = ""
    id_categoria: int = None
    nombre_categoria: str = ""  # Para facilitar la visualización, aunque no se almacena en la tabla productos
    id_marca: int = None
    nombre_marca: str = ""  # Para facilitar la visualización, aunque no se almacena en la tabla productos
    descripcion: str = ""
    precio_venta: float = 0.0
    precio_compra: float = 0.0
    existencia: int = 0
    id_proveedor: int = None
    nombre_proveedor: str = ""  # Para facilitar la visualización, aunque no se almacena en la tabla productos
    fecha_registro: datetime = None