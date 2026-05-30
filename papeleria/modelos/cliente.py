"""
Modelo: Cliente
Representa los datos de un cliente de la papelería.
"""


class Cliente:
    """Representa los datos de un cliente."""

    def __init__(self, id, nombre, telefono="", correo=""):
        self.id = id
        self.nombre = nombre
        self.telefono = telefono
        self.correo = correo

    def __str__(self):
        return self.nombre
