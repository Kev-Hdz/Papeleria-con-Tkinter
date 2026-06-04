from dtos import VentaDTO
from datos import VentaRepositorio, ProductoRepositorio

class VentaServicio:
    def __init__(self, venta_repositorio: VentaRepositorio, producto_repositorio: ProductoRepositorio):
        self.venta_repositorio = venta_repositorio
        self.producto_repositorio = producto_repositorio

    def registrar_nueva_venta(self, venta: VentaDTO) -> None:
        """Registra una nueva venta, validando que el carrito no esté vacío, que las cantidades sean positivas y que haya stock suficiente.
        Args:
            venta (VentaDTO): Objeto que representa la venta a registrar, incluyendo sus detalles.
        Raises:
            ValueError: Si el carrito está vacío, si alguna cantidad es negativa o si no hay stock suficiente para algún producto.
        """
        if not venta.detalles:
            raise ValueError("El carrito no puede estar vacío.")

        total_venta = 0.0
        for item in venta.detalles:
            if item.cantidad <= 0:
                raise ValueError(f"La cantidad para {item.nombre} debe ser mayor a cero.")
            if item.precio_unitario < 0:
                raise ValueError("El precio unitario no puede ser negativo.")

            producto_db = self.producto_repositorio.buscar_por_id(item.id_producto)
            if producto_db["existencia"] < item.cantidad:
                raise ValueError(f"Stock insuficiente para '{item.nombre}'. Quedan {producto_db['existencia']}.")
        
            total_venta += item.cantidad * item.precio_unitario
        venta.total = total_venta
        self.venta_repositorio.guardar_venta(venta)

    def consultar_ventas(self) -> list[VentaDTO]:
        """
        Obtiene el registro histórico de ventas realizadas. Sin detalles, solo la cabecera de cada venta.
            
        Returns:
            list[VentaDTO]: Lista de objetos VentaDTO representando las ventas registradas. Sin detalles. Si no hay ventas, devuelve una lista vacía.
        """
        return self.venta_repositorio.consultar()