
class Marca:
    """
    Clase que representa una marca de producto.
    
    Args:
        id (int): Identificador único de la marca.
        nombre (str): Nombre de la marca.
    """
    def __init__(self, nombre: str, id: int | None = None):
        self.id = id
        self.nombre = nombre

    def __str__(self):
        return self.nombre