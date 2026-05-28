"""
Vista: VistaVentas
Módulo gráfico para registrar nuevas ventas, agregar productos al carrito
y calcular el total automáticamente.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from modelos import DetalleVenta


class VistaVentas(tk.Frame):
    """Frame que contiene el módulo de registro de nueva venta."""

    def __init__(self, parent, almacen, utilidades, callback_post_venta=None):
        super().__init__(parent, bg="#f0f4f8")
        self.almacen = almacen
        self.ui = utilidades
        # Callback que ejecuta AppPapeleria tras registrar una venta
        # (refresca tabla de productos, tarjetas de inicio, etc.)
        self.callback_post_venta = callback_post_venta
        self._detalles = []     # carrito de la venta actual
        self._construir()

    def _construir(self):
        self.ui.titulo_seccion(self, "🛒 Nueva Venta")
        self._construir_selector_cliente()
        self._construir_selector_producto()
        self._construir_tabla_carrito()
        self._construir_pie()

    # ── Secciones de la vista ────────────────────────────────────────────────

    def _construir_selector_cliente(self):
        top = tk.Frame(self, bg="#f0f4f8")
        top.pack(fill="x", padx=15, pady=5)
        tk.Label(top, text="Cliente:", bg="#f0f4f8",
                 font=("Segoe UI", 10)).pack(side="left", padx=4)
        self.combo_cliente = ttk.Combobox(top, width=28, state="readonly",
                                          font=("Segoe UI", 10))
        self.actualizar_combo_clientes()
        self.combo_cliente.pack(side="left", padx=4)

    def _construir_selector_producto(self):
        sel = tk.LabelFrame(self, text="Agregar Producto",
                            font=("Segoe UI", 10, "bold"),
                            bg="#f0f4f8", fg="#1a237e", padx=10, pady=6)
        sel.pack(fill="x", padx=15, pady=4)

        tk.Label(sel, text="Producto:", bg="#f0f4f8",
                 font=("Segoe UI", 9)).grid(row=0, column=0, sticky="e", padx=4, pady=4)
        self.combo_producto = ttk.Combobox(sel, width=28, state="readonly",
                                           font=("Segoe UI", 10))
        self.combo_producto.grid(row=0, column=1, padx=4, pady=4)
        self.combo_producto.bind("<<ComboboxSelected>>", self._mostrar_precio)

        tk.Label(sel, text="Cantidad:", bg="#f0f4f8",
                 font=("Segoe UI", 9)).grid(row=0, column=2, sticky="e", padx=4)
        self.ent_cantidad = tk.Entry(sel, width=8, font=("Segoe UI", 10))
        self.ent_cantidad.grid(row=0, column=3, padx=4)

        tk.Label(sel, text="Precio Unit.:", bg="#f0f4f8",
                 font=("Segoe UI", 9)).grid(row=0, column=4, sticky="e", padx=4)
        self.lbl_precio = tk.Label(sel, text="$0.00", width=8,
                                    bg="#f0f4f8", font=("Segoe UI", 10, "bold"),
                                    fg="#2e7d32")
        self.lbl_precio.grid(row=0, column=5, padx=4)

        self.ui.boton(sel, "➕ Agregar", "#1565c0",
                      self._agregar_detalle).grid(row=0, column=6, padx=10)

        self.actualizar_combo_productos()

    def _construir_tabla_carrito(self):
        self.tabla = self.ui.crear_tabla(
            self, ("Producto", "Cant.", "Precio Unit.", "Subtotal"), height=6
        )

    def _construir_pie(self):
        pie = tk.Frame(self, bg="#f0f4f8")
        pie.pack(fill="x", padx=15, pady=4)
        self.lbl_total = tk.Label(pie, text="Total:  $0.00",
                                   font=("Segoe UI", 14, "bold"),
                                   bg="#f0f4f8", fg="#c62828")
        self.lbl_total.pack(side="right", padx=10)

        botones = tk.Frame(self, bg="#f0f4f8")
        botones.pack(pady=4)
        self.ui.boton(botones, "✅ Registrar Venta", "#2e7d32",
                      self.registrar_venta).pack(side="left", padx=8)
        self.ui.boton(botones, "❌ Cancelar / Limpiar", "#c62828",
                      self.limpiar_campos).pack(side="left", padx=8)

    # ── Métodos de negocio ───────────────────────────────────────────────────

    def _agregar_detalle(self):
        """Valida la selección y agrega un producto al carrito de la venta."""
        idx = self.combo_producto.current()
        if idx < 0:
            messagebox.showwarning("Sin producto", "Selecciona un producto.")
            return
        prod = self.almacen.productos[idx]
        try:
            cant = int(self.ent_cantidad.get())
            if cant <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Validación", "La cantidad debe ser un número entero positivo.")
            return
        if cant > prod.existencia:
            messagebox.showerror("Sin existencia",
                                  f"Solo hay {prod.existencia} unidades disponibles.")
            return

        det = DetalleVenta(prod, cant, prod.precio_venta)
        self._detalles.append(det)
        self.tabla.insert("", "end", values=(
            prod.nombre, cant, f"${prod.precio_venta:.2f}", f"${det.subtotal:.2f}"
        ))
        self._actualizar_total()
        self.ent_cantidad.delete(0, tk.END)
        self.combo_producto.set("")
        self.lbl_precio.config(text="$0.00")

    def registrar_venta(self):
        """Registra la venta en el almacén, descuenta existencias y limpia el formulario."""
        if not self._detalles:
            messagebox.showwarning("Sin productos", "Agrega al menos un producto a la venta.")
            return
        idx_cli = self.combo_cliente.current()
        cliente = self.almacen.clientes[idx_cli - 1] if idx_cli > 0 else None

        venta = self.almacen.registrar_venta(cliente, self._detalles)
        messagebox.showinfo("Venta registrada",
                             f"✅ Venta #{venta.id_venta} registrada.\nTotal: ${venta.total:.2f}")
        self.limpiar_campos()

        if self.callback_post_venta:
            self.callback_post_venta()

    def limpiar_campos(self):
        """Limpia el carrito y reinicia el formulario de venta."""
        self._detalles = []
        for row in self.tabla.get_children():
            self.tabla.delete(row)
        self.lbl_total.config(text="Total:  $0.00")
        self.ent_cantidad.delete(0, tk.END)
        self.combo_producto.set("")
        self.lbl_precio.config(text="$0.00")
        self.combo_cliente.current(0)

    def calcular_total(self):
        """Retorna el total de la venta actual sumando todos los subtotales."""
        return sum(d.subtotal for d in self._detalles)

    # ── Auxiliares ───────────────────────────────────────────────────────────

    def _mostrar_precio(self, event=None):
        """Muestra el precio de venta del producto seleccionado en el combo."""
        idx = self.combo_producto.current()
        if idx >= 0:
            self.lbl_precio.config(text=f"${self.almacen.productos[idx].precio_venta:.2f}")

    def _actualizar_total(self):
        self.lbl_total.config(text=f"Total:  ${self.calcular_total():.2f}")

    def actualizar_combo_clientes(self):
        """Refresca la lista de clientes en el combo."""
        nombres = ["— Sin cliente —"] + [c.nombre for c in self.almacen.clientes]
        self.combo_cliente["values"] = nombres
        self.combo_cliente.current(0)

    def actualizar_combo_productos(self):
        """Refresca la lista de productos disponibles en el combo."""
        self.combo_producto["values"] = [
            f"{p.nombre}  (Exist: {p.existencia})" for p in self.almacen.productos
        ]
