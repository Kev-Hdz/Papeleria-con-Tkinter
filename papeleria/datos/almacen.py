"""
Datos: Almacen
Gestiona todos los datos en memoria mientras no hay conexión a MySQL.
Actúa como repositorio central; cuando se integre MySQL, esta clase
se reemplazará por ConexionBD sin tocar el resto de la aplicación.
"""

from datetime import date
from modelos import Categoria, Proveedor, Cliente, ProductoPapeleria, DetalleVenta, Venta


class Almacen:
    """Simula la base de datos almacenando los datos en listas de Python."""

    def __init__(self):
        # Categorías predefinidas (equivale a la tabla `categorias`)
        self.categorias = [
            Categoria(1, "Cuadernos"),
            Categoria(2, "Escritura"),
            Categoria(3, "Oficina"),
            Categoria(4, "Manualidades"),
            Categoria(5, "Papeles"),
            Categoria(6, "Tecnología básica"),
            Categoria(7, "Otros"),
        ]
        self.proveedores = []
        self.clientes = []
        self.productos = []
        self.ventas = []

        # Contadores de ID (simulan el AUTO_INCREMENT de MySQL)
        self._id_proveedor = 1
        self._id_cliente = 1
        self._id_producto = 1
        self._id_venta = 1

        # Carga datos de ejemplo para pruebas
        self._cargar_datos_ejemplo()

    # ── Proveedores ──────────────────────────────────────────────────────────

    def registrar_proveedor(self, nombre, telefono, correo, direccion):
        """Crea y guarda un nuevo proveedor. Retorna el objeto creado."""
        p = Proveedor(self._id_proveedor, nombre, telefono, correo, direccion)
        self.proveedores.append(p)
        self._id_proveedor += 1
        return p

    def obtener_proveedores(self):
        """Retorna la lista completa de proveedores."""
        return self.proveedores

    # ── Clientes ─────────────────────────────────────────────────────────────

    def registrar_cliente(self, nombre, telefono, correo):
        """Crea y guarda un nuevo cliente. Retorna el objeto creado."""
        c = Cliente(self._id_cliente, nombre, telefono, correo)
        self.clientes.append(c)
        self._id_cliente += 1
        return c

    def obtener_clientes(self):
        """Retorna la lista completa de clientes."""
        return self.clientes

    # ── Productos ────────────────────────────────────────────────────────────

    def registrar_producto(self, nombre, categoria, marca, descripcion,
                           precio_compra, precio_venta, existencia, proveedor):
        """Crea y guarda un nuevo producto con la fecha de hoy. Retorna el objeto."""
        fecha = date.today().strftime("%Y-%m-%d")
        p = ProductoPapeleria(
            self._id_producto, nombre, categoria, marca, descripcion,
            precio_compra, precio_venta, existencia, proveedor, fecha
        )
        self.productos.append(p)
        self._id_producto += 1
        return p

    def consultar_productos(self):
        """Retorna la lista completa de productos."""
        return self.productos

    def buscar_producto(self, texto):
        """Busca productos por nombre, categoría o proveedor (texto libre)."""
        texto = texto.lower()
        return [
            p for p in self.productos
            if texto in p.nombre.lower()
            or texto in p.categoria.nombre_categoria.lower()
            or (p.proveedor and texto in p.proveedor.nombre.lower())
        ]

    def actualizar_producto(self, id_producto, nombre, categoria, marca, descripcion,
                            precio_compra, precio_venta, existencia, proveedor):
        """Modifica los datos de un producto existente. Retorna True si lo encontró."""
        for p in self.productos:
            if p.id_producto == id_producto:
                p.nombre = nombre
                p.categoria = categoria
                p.marca = marca
                p.descripcion = descripcion
                p.precio_compra = float(precio_compra)
                p.precio_venta = float(precio_venta)
                p.existencia = int(existencia)
                p.proveedor = proveedor
                return True
        return False

    def eliminar_producto(self, id_producto):
        """Elimina un producto por ID. Retorna True si lo encontró."""
        for i, p in enumerate(self.productos):
            if p.id_producto == id_producto:
                self.productos.pop(i)
                return True
        return False

    def obtener_producto_por_id(self, id_producto):
        """Retorna el producto con el ID indicado, o None si no existe."""
        for p in self.productos:
            if p.id_producto == id_producto:
                return p
        return None

    # ── Ventas ───────────────────────────────────────────────────────────────

    def registrar_venta(self, cliente, detalles):
        """
        Registra una venta, agrega sus detalles y descuenta
        las existencias de cada producto vendido.
        """
        v = Venta(self._id_venta, date.today().strftime("%Y-%m-%d"), cliente)
        for det in detalles:
            v.agregar_detalle(det)
            det.producto.existencia -= det.cantidad
        self.ventas.append(v)
        self._id_venta += 1
        return v

    def obtener_ventas(self):
        """Retorna la lista completa de ventas registradas."""
        return self.ventas

    # ── Datos de ejemplo ─────────────────────────────────────────────────────

    def _cargar_datos_ejemplo(self):
        """Inserta datos de prueba para poder usar la app sin MySQL."""
        prov1 = self.registrar_proveedor(
            "Distribuidora Norma", "9931234567",
            "norma@ejemplo.com", "Calle 20 #45, Col. Centro"
        )
        prov2 = self.registrar_proveedor(
            "Pelikan México", "9939876543",
            "pelikan@ejemplo.com", "Av. Reforma #100"
        )
        self.registrar_cliente("Juan Pérez", "9931112233", "juan@email.com")
        self.registrar_cliente("María López", "9934445566", "maria@email.com")

        self.registrar_producto(
            "Cuaderno profesional", self.categorias[0], "Norma",
            "100 hojas, raya francesa", 15.00, 28.00, 50, prov1
        )
        self.registrar_producto(
            "Pluma azul BIC", self.categorias[1], "BIC",
            "Tinta azul punta media", 3.50, 7.00, 120, prov2
        )
        self.registrar_producto(
            "Colores Pelikan x12", self.categorias[3], "Pelikan",
            "Colores de madera surtidos", 28.00, 55.00, 35, prov2
        )
