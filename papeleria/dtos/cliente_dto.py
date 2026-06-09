from dataclasses import dataclass

@dataclass
class ClienteDTO:
    id_cliente: int = None  # Se asignará automáticamente al insertar en la base de datos
    nombre: str = ""
    telefono: str = ""
    correo: str = ""