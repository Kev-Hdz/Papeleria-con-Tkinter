from db import DatabaseManager
from dtos import VentaDTO, DetalleVentaDTO


class VentaRepositorio:
    def __init__(self, db_config: dict):
        self.db_config = db_config

    def guardar_venta(self, venta: VentaDTO) -> int:
        """Guarda una venta completa, incluyendo su cabecera y detalles, en la base de datos.
        Args:
            venta (VentaDTO): Objeto que representa la cabecera de la venta.
        Returns:
            int: El ID de la venta recién creada.
        """
        from datetime import datetime
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with DatabaseManager(self.db_config) as cursor:
            try:
                # Insertar cabecera de la venta
                cursor.execute(
                    "INSERT INTO ventas (id_cliente, fecha_venta, total) VALUES (%s, %s, %s)",
                    (venta.id_cliente, fecha_actual, venta.total)
                )
                id_venta = cursor.lastrowid
                
                # Insertar detalles y actualizar stock
                for item in venta.detalles:
                    cursor.execute(
                        "INSERT INTO detalle_venta (id_venta, id_producto, cantidad, precio_unitario) VALUES (%s, %s, %s, %s)",
                        (id_venta, item.id_producto, item.cantidad, item.precio_unitario)
                    )
                    
                    cursor.execute(
                        "UPDATE productos SET existencia = existencia - %s WHERE id_producto = %s",
                        (item.cantidad, item.id_producto)
                    )
                
                return id_venta
            
            except Exception as e:
                raise e
            
    def consultar(self) -> list[VentaDTO]:
        """
        Recupera el listado de ventas maestras (sin sus detalles) usando JOINs 
        para traer el nombre del cliente.
        
        Returns:
            list[VentaDTO]: Lista de objetos VentaDTO representando la cabecera de las ventas.
        """
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute("""SELECT v.id_venta,
                                             v.fecha_venta,
                                             v.id_cliente,
                                             c.nombre AS nombre_cliente,
                                             v.total
                                      FROM ventas v
                                      JOIN clientes c ON v.id_cliente = c.id_cliente""")
            return [VentaDTO(**row) for row in cursor.fetchall()]
            

       
    def consultar_detalles(self, id_venta: int) -> list[DetalleVentaDTO]:
        """
        Recupera los renglones (detalles) específicos asociados a una venta.
        
        Args:
            id_venta (int): ID maestro de la venta.
            
        Returns:
            list[DetalleVentaDTO]: Lista de objetos DetalleVentaDTO representando los detalles de la venta.
        """
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute("""SELECT dv.id_detalle,
                                             dv.id_venta,
                                             dv.id_producto,
                                             p.nombre AS nombre_producto,
                                             dv.cantidad,
                                             dv.precio_unitario,
                                             (dv.cantidad * dv.precio_unitario) AS subtotal
                                      FROM detalle_venta dv
                                      JOIN productos p ON dv.id_producto = p.id_producto
                                      WHERE dv.id_venta = %s""", (id_venta,))
            return [DetalleVentaDTO(**row) for row in cursor.fetchall()]   