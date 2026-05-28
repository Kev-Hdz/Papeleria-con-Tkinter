"""
Vista: VistaProductos
Módulo gráfico para registrar, consultar, buscar, actualizar y eliminar productos.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from modelos import DetalleVenta


class VistaProductos(tk.Frame):
    """Frame que contiene todo el módulo de gestión de productos."""

    def __init__(self, parent, almacen, utilidades):
        super().__init__(parent, bg="#f0f4f8")
        self.almacen = almacen
        self.ui = utilidades        # métodos auxiliares compartidos (titulo, boton, tabla)
        self._construir()

    def _construir(self):
        self.ui.titulo_seccion(self, "📦 Gestión de Productos")
        self._construir_formulario()
        self._construir_buscador()
        self.tabla = self.ui.crear_tabla(
            self,
            ("ID", "Nombre", "Categoría", "Marca", "P.Compra",
             "P.Venta", "Existencia", "Proveedor", "Fecha Registro")
        )
        self.tabla.bind("<ButtonRelease-1>", self._seleccionar_fila)
        self.consultar_productos()

    # ── Formulario ───────────────────────────────────────────────────────────

    def _construir_formulario(self):
        form = tk.LabelFrame(self, text="Datos del Producto",
                             font=("Segoe UI", 10, "bold"),
                             bg="#f0f4f8", fg="#1a237e", padx=10, pady=8)
        form.pack(fill="x", padx=15, pady=(5, 3))

        # Columna izquierda — campos de texto
        col_izq = tk.Frame(form, bg="#f0f4f8")
        col_izq.pack(side="left", padx=8)
        campos = [("Nombre:", "ent_nombre"), ("Marca:", "ent_marca"),
                  ("Precio Compra $:", "ent_precio_compra"),
                  ("Precio Venta $:", "ent_precio_venta"),
                  ("Existencia:", "ent_existencia")]
        for i, (lbl, attr) in enumerate(campos):
            tk.Label(col_izq, text=lbl, bg="#f0f4f8",
                     font=("Segoe UI", 9)).grid(row=i, column=0, sticky="e", pady=3, padx=4)
            ent = tk.Entry(col_izq, width=22, font=("Segoe UI", 10))
            ent.grid(row=i, column=1, sticky="w", pady=3)
            setattr(self, attr, ent)

        # Columna derecha — combos y descripción
        col_der = tk.Frame(form, bg="#f0f4f8")
        col_der.pack(side="left", padx=8)

        tk.Label(col_der, text="Categoría:", bg="#f0f4f8",
                 font=("Segoe UI", 9)).grid(row=0, column=0, sticky="e", pady=3, padx=4)
        self.combo_categoria = ttk.Combobox(col_der, width=20, state="readonly",
                                             font=("Segoe UI", 10))
        self.combo_categoria["values"] = [c.nombre_categoria
                                           for c in self.almacen.categorias]
        self.combo_categoria.grid(row=0, column=1, sticky="w", pady=3)

        tk.Label(col_der, text="Proveedor:", bg="#f0f4f8",
                 font=("Segoe UI", 9)).grid(row=1, column=0, sticky="e", pady=3, padx=4)
        self.combo_proveedor = ttk.Combobox(col_der, width=20, state="readonly",
                                             font=("Segoe UI", 10))
        self.actualizar_combo_proveedores()
        self.combo_proveedor.grid(row=1, column=1, sticky="w", pady=3)

        tk.Label(col_der, text="Descripción:", bg="#f0f4f8",
                 font=("Segoe UI", 9)).grid(row=2, column=0, sticky="ne", pady=3, padx=4)
        self.txt_descripcion = tk.Text(col_der, width=22, height=3,
                                        font=("Segoe UI", 10))
        self.txt_descripcion.grid(row=2, column=1, rowspan=3, sticky="w", pady=3)

        # Botones de acción
        btn_frame = tk.Frame(form, bg="#f0f4f8")
        btn_frame.pack(side="left", padx=16, anchor="n", pady=6)
        self.ui.boton(btn_frame, "💾 Registrar",  "#2e7d32", self.registrar_producto).pack(fill="x", pady=3)
        self.ui.boton(btn_frame, "✏️ Actualizar", "#1565c0", self.actualizar_producto).pack(fill="x", pady=3)
        self.ui.boton(btn_frame, "🗑️ Eliminar",   "#c62828", self.eliminar_producto).pack(fill="x", pady=3)
        self.ui.boton(btn_frame, "🧹 Limpiar",    "#546e7a", self.limpiar_campos).pack(fill="x", pady=3)

    def _construir_buscador(self):
        bus = tk.Frame(self, bg="#f0f4f8")
        bus.pack(fill="x", padx=15, pady=3)
        tk.Label(bus, text="🔍 Buscar:", bg="#f0f4f8",
                 font=("Segoe UI", 10)).pack(side="left")
        self.ent_buscar = tk.Entry(bus, width=30, font=("Segoe UI", 10))
        self.ent_buscar.pack(side="left", padx=6)
        self.ui.boton(bus, "Buscar",       "#1a237e", self.buscar_producto).pack(side="left", padx=3)
        self.ui.boton(bus, "Mostrar todos","#455a64", self.consultar_productos).pack(side="left", padx=3)

    # ── Métodos de negocio ───────────────────────────────────────────────────

    def registrar_producto(self):
        """Captura los campos y guarda un nuevo producto en el almacén."""
        if not self._validar_campos():
            return
        datos = self._leer_campos()
        self.almacen.registrar_producto(**datos)
        messagebox.showinfo("Éxito", f"Producto '{datos['nombre']}' registrado correctamente.")
        self.limpiar_campos()
        self.consultar_productos()

    def consultar_productos(self):
        """Muestra todos los productos registrados en la tabla."""
        self._rellenar_tabla(self.almacen.consultar_productos())

    def buscar_producto(self):
        """Filtra los productos según el texto de búsqueda."""
        texto = self.ent_buscar.get().strip()
        resultados = self.almacen.buscar_producto(texto) if texto else self.almacen.consultar_productos()
        self._rellenar_tabla(resultados)

    def actualizar_producto(self):
        """Modifica los datos del producto seleccionado en la tabla."""
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Sin selección", "Selecciona un producto de la tabla.")
            return
        if not self._validar_campos():
            return
        id_prod = int(self.tabla.item(seleccion[0])["values"][0])
        datos = self._leer_campos()
        self.almacen.actualizar_producto(id_prod, **datos)
        messagebox.showinfo("Éxito", "Producto actualizado correctamente.")
        self.limpiar_campos()
        self.consultar_productos()

    def eliminar_producto(self):
        """Elimina el producto seleccionado tras confirmación del usuario."""
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Sin selección", "Selecciona un producto de la tabla.")
            return
        valores = self.tabla.item(seleccion[0])["values"]
        id_prod, nombre = int(valores[0]), valores[1]
        if messagebox.askyesno("Confirmar",
                                f"¿Eliminar el producto '{nombre}'?\nEsta acción no se puede deshacer."):
            self.almacen.eliminar_producto(id_prod)
            messagebox.showinfo("Eliminado", "Producto eliminado correctamente.")
            self.limpiar_campos()
            self.consultar_productos()

    def limpiar_campos(self):
        """Limpia todas las cajas de texto del formulario."""
        for attr in ["ent_nombre", "ent_marca", "ent_precio_compra",
                     "ent_precio_venta", "ent_existencia"]:
            getattr(self, attr).delete(0, tk.END)
        self.txt_descripcion.delete("1.0", tk.END)
        self.combo_categoria.set("")
        self.combo_proveedor.set("")

    # ── Auxiliares ───────────────────────────────────────────────────────────

    def actualizar_combo_proveedores(self):
        """Refresca la lista de proveedores en el combo (llamado tras registrar uno nuevo)."""
        self.combo_proveedor["values"] = [p.nombre for p in self.almacen.proveedores]

    def _leer_campos(self):
        """Lee y retorna los valores del formulario como dict listo para el almacén."""
        idx_cat = self.combo_categoria.current()
        idx_prov = self.combo_proveedor.current()
        return {
            "nombre": self.ent_nombre.get().strip(),
            "categoria": self.almacen.categorias[idx_cat],
            "marca": self.ent_marca.get().strip(),
            "descripcion": self.txt_descripcion.get("1.0", tk.END).strip(),
            "precio_compra": float(self.ent_precio_compra.get()),
            "precio_venta": float(self.ent_precio_venta.get()),
            "existencia": int(self.ent_existencia.get()),
            "proveedor": (self.almacen.proveedores[idx_prov]
                          if idx_prov >= 0 and self.almacen.proveedores else None),
        }

    def _validar_campos(self):
        """Revisa que los campos del formulario sean válidos antes de operar."""
        if not self.ent_nombre.get().strip():
            messagebox.showerror("Validación", "El nombre del producto es obligatorio.")
            return False
        if self.combo_categoria.get() == "":
            messagebox.showerror("Validación", "Debes seleccionar una categoría.")
            return False
        try:
            if float(self.ent_precio_compra.get()) <= 0 or float(self.ent_precio_venta.get()) <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Validación", "Los precios deben ser números mayores a cero.")
            return False
        try:
            if int(self.ent_existencia.get()) < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Validación", "La existencia debe ser un número entero ≥ 0.")
            return False
        return True

    def _seleccionar_fila(self, event=None):
        """Carga en el formulario los datos del producto seleccionado en la tabla."""
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        id_prod = int(self.tabla.item(seleccion[0])["values"][0])
        prod = self.almacen.obtener_producto_por_id(id_prod)
        if not prod:
            return
        self.limpiar_campos()
        self.ent_nombre.insert(0, prod.nombre)
        self.ent_marca.insert(0, prod.marca)
        self.ent_precio_compra.insert(0, str(prod.precio_compra))
        self.ent_precio_venta.insert(0, str(prod.precio_venta))
        self.ent_existencia.insert(0, str(prod.existencia))
        self.txt_descripcion.insert("1.0", prod.descripcion)
        self.combo_categoria.set(prod.categoria.nombre_categoria)
        if prod.proveedor:
            self.combo_proveedor.set(prod.proveedor.nombre)

    def _rellenar_tabla(self, productos):
        """Limpia la tabla y la rellena con la lista de productos indicada."""
        for row in self.tabla.get_children():
            self.tabla.delete(row)
        for p in productos:
            prov = p.proveedor.nombre if p.proveedor else "—"
            self.tabla.insert("", "end", values=(
                p.id_producto, p.nombre, p.categoria.nombre_categoria, p.marca,
                f"${p.precio_compra:.2f}", f"${p.precio_venta:.2f}",
                p.existencia, prov, p.fecha_registro
            ))
