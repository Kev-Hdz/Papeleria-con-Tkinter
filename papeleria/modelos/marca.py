
class Marca:
    def __init__(self, id: int, nombre: str):
        self.id = id
        self.nombre = nombre

    def __str__(self):
        return self.nombre