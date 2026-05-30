"""
Modelo: Categoria
Representa la clasificación de los productos de la papelería.
"""


class Categoria:
    """Representa la clasificación de los productos."""

    def __init__(self, id_categoria, nombre_categoria):
        self.id = id_categoria
        self.nombre = nombre_categoria

    def __str__(self):
        return self.nombre
