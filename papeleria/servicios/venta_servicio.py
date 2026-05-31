from datetime import datetime
from modelos import Venta, DetalleVenta

class VentaServicio:
    """
    Orquestador del módulo de ventas. 
    Recibe el carrito de compras de la UI, aplica reglas de negocio usando los modelos
    de dominio y envía los datos validados al repositorio.
        - Es el único que conoce los modelos de dominio (Venta, DetalleVenta, ProductoPapeleria).
        
    """
    def __init__(self, venta_repositorio, producto_repositorio):
        self.venta_repo = venta_repositorio
        self.producto_repo = producto_repositorio

  
    
    def procesar_venta(self, id_cliente: int | None, carrito: list[dict]) -> int:
        """
        Ejecuta la venta.
        
        Args:
            id_cliente: El ID del cliente (None si es venta al público en general).
            carrito: Una lista de diccionarios con los items de la venta.
                        Ejemplo: [{'producto_id': 1, 'cantidad': 2}, {'producto_id': 5, 'cantidad': 1}]
        
        Returns:
            int: El ID de la venta generada.
        """
        # 1. Creamos la venta con los datos básicos (fecha, cliente)
        nueva_venta = Venta(fecha_venta=datetime.now(), id_cliente=id_cliente)

        # 2. Procesamos cada línea del carrito
        for item in carrito:
            producto_id = item['producto_id']
            cantidad_solicitada = int(item['cantidad'])

            producto = self.producto_repo.buscar_por_id(producto_id)
            
            if not producto:
                raise ValueError(f"El producto con ID {producto_id} no existe o fue eliminado.")

            # Regla de negocio: ¿Hay stock suficiente? 
            producto.descontar_existencia(cantidad_solicitada)

            detalle = DetalleVenta(
                producto_id=producto.id,
                cantidad=cantidad_solicitada,
                precio_unitario=producto.precio_venta 
            )
            
            # Agregamos el detalle a la venta (la venta recalcula su total sola)
            nueva_venta.agregar_detalle(detalle)

        # 3. Validamos la venta completa antes de guardarla
        nueva_venta.validar_venta()

        id_venta_generada = self.venta_repo.guardar_venta(nueva_venta)
        
        return id_venta_generada


    def obtener_historial(self) -> list[dict]:
        """
        Obtiene el historial de ventas para mostrar en la UI.
        
        Returns:
            list[dict]: Una lista de diccionarios con la información de cada venta.
        """
        return self.venta_repo.obtener_todas_las_ventas()