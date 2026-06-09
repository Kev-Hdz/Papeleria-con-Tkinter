from dataclasses import dataclass

@dataclass
class ProveedorDTO:
    id_proveedor: int = None  # Se asignará automáticamente al insertar en la base de datos
    nombre: str = ""
    telefono: str = ""
    correo: str = ""
    direccion: str = ""
