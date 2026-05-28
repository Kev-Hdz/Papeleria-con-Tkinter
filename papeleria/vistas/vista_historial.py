"""
Vista: VistaHistorial
Módulo gráfico para consultar el historial de ventas y ver el detalle de cada una.
"""

import tkinter as tk


class VistaHistorial(tk.Frame):
    """Frame que muestra el historial de ventas y el detalle de la venta seleccionada."""

    def __init__(self, parent, almacen, utilidades):
        super().__init__(parent, bg="#f0f4f8")
        self.almacen = almacen
        self.ui = utilidades
        self._construir()

    def _construir(self):
        self.ui.titulo_seccion(self, "📋 Historial de Ventas")
        self.ui.boton(self, "🔄 Actualizar historial", "#1a237e",
                      self.refrescar).pack(anchor="e", padx=15, pady=5)

        self.tabla_ventas = self.ui.crear_tabla(
            self, ("ID Venta", "Fecha", "Cliente", "Total"), height=8
        )
        self.tabla_ventas.bind("<ButtonRelease-1>", self._mostrar_detalle)

        det = tk.LabelFrame(self, text="Detalle de la Venta Seleccionada",
                            font=("Segoe UI", 10, "bold"),
                            bg="#f0f4f8", fg="#1a237e", padx=8, pady=6)
        det.pack(fill="both", expand=True, padx=15, pady=5)
        self.tabla_detalle = self.ui.crear_tabla(
            det, ("Producto", "Cantidad", "Precio Unit.", "Subtotal"), height=5
        )
        self.refrescar()

    # ── Métodos de negocio ───────────────────────────────────────────────────

    def refrescar(self):
        """Recarga la tabla de ventas con los datos actuales del almacén."""
        for row in self.tabla_ventas.get_children():
            self.tabla_ventas.delete(row)
        for v in self.almacen.obtener_ventas():
            cliente = v.cliente.nombre if v.cliente else "— Público general —"
            self.tabla_ventas.insert("", "end",
                values=(v.id_venta, v.fecha_venta, cliente, f"${v.total:.2f}"))

    # ── Auxiliares ───────────────────────────────────────────────────────────

    def _mostrar_detalle(self, event=None):
        """Muestra los productos de la venta seleccionada en la tabla de detalle."""
        seleccion = self.tabla_ventas.selection()
        if not seleccion:
            return
        id_venta = int(self.tabla_ventas.item(seleccion[0])["values"][0])
        venta = next((v for v in self.almacen.ventas if v.id_venta == id_venta), None)
        if not venta:
            return
        for row in self.tabla_detalle.get_children():
            self.tabla_detalle.delete(row)
        for det in venta.detalles:
            self.tabla_detalle.insert("", "end", values=(
                det.producto.nombre, det.cantidad,
                f"${det.precio_unitario:.2f}", f"${det.subtotal:.2f}"
            ))
