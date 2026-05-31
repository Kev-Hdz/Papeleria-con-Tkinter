"""
Modelo: Cliente
Representa los datos de un cliente de la papelería.
"""


class Cliente:
    """
    Representa los datos de un cliente.
    
    Args:
        id (int): Identificador único del cliente.
        nombre (str): Nombre del cliente.
        telefono (str): Número de teléfono del cliente.
        correo (str): Dirección de correo electrónico del cliente.
    """

    def __init__(self, nombre: str, telefono: str = "", correo: str = "", id: int | None = None):
        self.id = id
        self.nombre = nombre
        self.telefono = telefono
        self.correo = correo

    def __str__(self):
        return self.nombre
