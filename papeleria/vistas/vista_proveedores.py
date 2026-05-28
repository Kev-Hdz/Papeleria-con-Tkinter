"""
Vista: VistaProveedores
Módulo gráfico para registrar y consultar proveedores.
"""

import tkinter as tk
from tkinter import messagebox


class VistaProveedores(tk.Frame):
    """Frame que contiene todo el módulo de gestión de proveedores."""

    def __init__(self, parent, almacen, utilidades, callback_actualizar_combo=None):
        super().__init__(parent, bg="#f0f4f8")
        self.almacen = almacen
        self.ui = utilidades
        # Callback para notificar a VistaProductos que refresque su combo de proveedores
        self.callback_actualizar_combo = callback_actualizar_combo
        self._construir()

    def _construir(self):
        self.ui.titulo_seccion(self, "🚚 Gestión de Proveedores")
        self._construir_formulario()
        self.tabla = self.ui.crear_tabla(
            self, ("ID", "Nombre", "Teléfono", "Correo", "Dirección")
        )
        self._rellenar_tabla()

    def _construir_formulario(self):
        form = tk.LabelFrame(self, text="Datos del Proveedor",
                             font=("Segoe UI", 10, "bold"),
                             bg="#f0f4f8", fg="#1a237e", padx=10, pady=8)
        form.pack(fill="x", padx=15, pady=5)

        col = tk.Frame(form, bg="#f0f4f8")
        col.pack(side="left", padx=8)
        campos = [("Nombre:", "ent_nombre"), ("Teléfono:", "ent_telefono"),
                  ("Correo:", "ent_correo"), ("Dirección:", "ent_direccion")]
        for i, (lbl, attr) in enumerate(campos):
            tk.Label(col, text=lbl, bg="#f0f4f8",
                     font=("Segoe UI", 9)).grid(row=i, column=0, sticky="e", pady=4, padx=4)
            ent = tk.Entry(col, width=30, font=("Segoe UI", 10))
            ent.grid(row=i, column=1, sticky="w", pady=4)
            setattr(self, attr, ent)

        btn_frame = tk.Frame(form, bg="#f0f4f8")
        btn_frame.pack(side="left", padx=16, anchor="n", pady=6)
        self.ui.boton(btn_frame, "💾 Registrar Proveedor", "#2e7d32",
                      self.registrar_proveedor).pack(fill="x", pady=3)
        self.ui.boton(btn_frame, "🧹 Limpiar", "#546e7a",
                      self.limpiar_campos).pack(fill="x", pady=3)

    # ── Métodos de negocio ───────────────────────────────────────────────────

    def registrar_proveedor(self):
        """Valida los campos y registra un nuevo proveedor en el almacén."""
        nombre = self.ent_nombre.get().strip()
        if not nombre:
            messagebox.showerror("Validación", "El nombre del proveedor es obligatorio.")
            return
        tel = self.ent_telefono.get().strip()
        if tel and not tel.isdigit():
            messagebox.showerror("Validación", "El teléfono debe contener solo números.")
            return
        correo = self.ent_correo.get().strip()
        direccion = self.ent_direccion.get().strip()

        self.almacen.registrar_proveedor(nombre, tel, correo, direccion)
        messagebox.showinfo("Éxito", f"Proveedor '{nombre}' registrado correctamente.")
        self.limpiar_campos()
        self._rellenar_tabla()

        # Notifica a VistaProductos para que refresque su combo de proveedores
        if self.callback_actualizar_combo:
            self.callback_actualizar_combo()

    def limpiar_campos(self):
        """Limpia todos los campos del formulario."""
        for attr in ["ent_nombre", "ent_telefono", "ent_correo", "ent_direccion"]:
            getattr(self, attr).delete(0, tk.END)

    # ── Auxiliares ───────────────────────────────────────────────────────────

    def _rellenar_tabla(self):
        """Limpia y rellena la tabla con todos los proveedores registrados."""
        for row in self.tabla.get_children():
            self.tabla.delete(row)
        for p in self.almacen.obtener_proveedores():
            self.tabla.insert("", "end",
                values=(p.id_proveedor, p.nombre, p.telefono, p.correo, p.direccion))
