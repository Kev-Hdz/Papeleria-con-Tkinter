"""
Modelo: Categoria
Representa la clasificación de los productos de la papelería.
"""


class Categoria:
    """
    Representa la clasificación de los productos.
    
    Args:
        id (int): Identificador único de la categoría.
        nombre (str): Nombre de la categoría.
    
    """

    def __init__(self, nombre: str, id: int | None = None):
        self.id = id
        self.nombre = nombre    

    def __str__(self):
        return self.nombre
