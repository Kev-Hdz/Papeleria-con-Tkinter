from db import DatabaseManager
from modelos import Venta

class VentaRepositorio:
    """
    Repositorio transaccional para el módulo de ventas.
    Garantiza que la venta, sus detalles y la actualización de inventario 
    se guarden como un bloque único o no se guarden en absoluto.
    """
    def __init__(self, db_config):
        self.db_config = db_config

    # ==========================================
    # 1. ESCRITURA (Transaccional)
    # ==========================================

    def guardar_venta(self, venta: Venta) -> int:
        """
        Inserta la cabecera, los detalles y actualiza el stock físico en MySQL.
        
        Args:
            venta (Venta): El objeto de dominio rico ya validado por el Servicio.
            
        Returns:
            int: El ID autogenerado de la nueva venta.
        """
        # Consultas preparadas
        sql_venta = """
            INSERT INTO ventas (fecha_venta, id_cliente, total) 
            VALUES (%s, %s, %s);
        """
        
        sql_detalle = """
            INSERT INTO detalle_venta (id_venta, id_producto, cantidad, precio_unitario, subtotal) 
            VALUES (%s, %s, %s, %s, %s);
        """
        
        # Sincronizamos la base de datos restándole al stock actual
        sql_stock = """
            UPDATE productos 
            SET existencia = existencia - %s 
            WHERE id_producto = %s;
        """

        with DatabaseManager(self.db_config) as cursor:
            # 1. Guardamos la cabecera (Tabla: ventas)
            cursor.execute(sql_venta, (
                venta.fecha_venta, 
                venta.id_cliente, 
                venta.total
            ))
            
            # Recuperamos el ID que MySQL le acaba de asignar a esta venta
            id_venta_generado = cursor.lastrowid

            # 2. Guardamos las líneas y afectamos el inventario
            for detalle in venta.detalles:
                # Insertar en detalle_venta
                cursor.execute(sql_detalle, (
                    id_venta_generado,
                    detalle.producto_id,
                    detalle.cantidad,
                    detalle.precio_unitario,
                    detalle.subtotal
                ))
                
                # Actualizar el stock en la tabla productos
                cursor.execute(sql_stock, (
                    detalle.cantidad, 
                    detalle.producto_id
                ))

            # Al terminar el ciclo y salir del bloque 'with', tu DatabaseManager
            # ejecutará self.connection.commit() automáticamente.
            return id_venta_generado


    # ==========================================
    # 2. LECTURA (Consultas Rápidas para UI)
    # ==========================================

    def obtener_todas_las_ventas(self) -> list[dict]:
        """
        Para llenar el 'Historial de Ventas' en Tkinter.
        Hace un JOIN con clientes para mostrar el nombre en lugar de un número.
        """
        query = """
            SELECT 
                v.id_venta, 
                v.fecha_venta, 
                v.total, 
                c.nombre AS nombre_cliente
            FROM ventas v
            LEFT JOIN clientes c ON v.id_cliente = c.id_cliente
            ORDER BY v.fecha_venta DESC;
        """
        
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute(query)
            # Devuelve diccionarios listos para inyectar en el Treeview
            return cursor.fetchall()

    def obtener_detalles_por_venta(self, id_venta: int) -> list[dict]:
        """
        Opcional: Por si el usuario hace doble clic en una venta del historial 
        y quiere ver qué productos se llevaron exactamente en ese ticket.
        """
        query = """
            SELECT 
                d.id_detalle,
                p.nombre AS nombre_producto,
                d.cantidad,
                d.precio_unitario,
                d.subtotal
            FROM detalle_venta d
            INNER JOIN productos p ON d.id_producto = p.id_producto
            WHERE d.id_venta = %s;
        """
        
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute(query, (id_venta,))
            return cursor.fetchall()