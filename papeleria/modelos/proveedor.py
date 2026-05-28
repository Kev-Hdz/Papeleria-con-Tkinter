"""
Modelo: Proveedor
Representa los datos de un proveedor que surte productos a la papelería.
"""


class Proveedor:
    """Representa los datos de un proveedor."""

    def __init__(self, id_proveedor, nombre, telefono="", correo="", direccion=""):
        self.id_proveedor = id_proveedor
        self.nombre = nombre
        self.telefono = telefono
        self.correo = correo
        self.direccion = direccion

    def __str__(self):
        return self.nombre
