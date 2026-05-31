
class Proveedor:
    """
    Representa los datos de un proveedor.
    
    Args:
        id (int): Identificador único del proveedor.
        nombre (str): Nombre del proveedor.
        telefono (str): Número de teléfono del proveedor.
        correo (str): Dirección de correo electrónico del proveedor.
        direccion (str): Dirección física del proveedor.
    """

    def __init__(self, nombre: str, telefono: str = "", correo: str = "", direccion: str = "", id: int | None = None):
        self.id = id
        self.nombre = nombre
        self.telefono = telefono
        self.correo = correo
        self.direccion = direccion

    def __str__(self):
        return self.nombre
