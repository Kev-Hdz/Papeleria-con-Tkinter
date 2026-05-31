from modelos import Cliente, Proveedor
from datos import ContactoRepositorio
class ContactoServicio:
    def __init__(self, contacto_repositorio: ContactoRepositorio):
        self.repositorio = contacto_repositorio

    def agregar_cliente(self, datos_cliente: dict):
        cliente = Cliente(**datos_cliente)
        self.repositorio.agregar_cliente(cliente)

    def agregar_proveedor(self, datos_proveedor: dict):
        proveedor = Proveedor(**datos_proveedor)
        self.repositorio.agregar_proveedor(proveedor)

    def obtener_clientes(self):
        return self.repositorio.obtener_clientes()

    def obtener_proveedores(self):
        return self.repositorio.obtener_proveedores()