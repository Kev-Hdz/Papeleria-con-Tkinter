"""
Aplicación Gráfica para Gestión de Papelería
=============================================
Punto de entrada y clase principal de la aplicación.

Estructura del proyecto:
    papeleria/
    ├── main.py                   ← Este archivo (clase AppPapeleria + arranque)
    ├── modelos/
    │   ├── __init__.py
    │   ├── categoria.py          ← Clase Categoria
    │   ├── cliente.py            ← Clase Cliente
    │   ├── producto.py           ← Clase ProductoPapeleria
    │   ├── proveedor.py          ← Clase Proveedor
    │   └── venta.py              ← Clases Venta y DetalleVenta
    ├── datos/
    │   ├── __init__.py
    │   └── almacen.py            ← Clase Almacen (repositorio en memoria)
    └── vistas/
        ├── __init__.py
        ├── utilidades.py         ← Helpers de UI compartidos
        ├── vista_productos.py    ← Módulo Productos
        ├── vista_proveedores.py  ← Módulo Proveedores
        ├── vista_clientes.py     ← Módulo Clientes
        ├── vista_ventas.py       ← Módulo Nueva Venta
        └── vista_historial.py    ← Módulo Historial de Ventas

Ejecución:
    python main.py
"""

import tkinter as tk
from tkinter import ttk, messagebox

from datos import Almacen
from vistas import (Utilidades, VistaProductos, VistaProveedores,
                    VistaClientes, VistaVentas, VistaHistorial)


class AppPapeleria(tk.Tk):
    """
    Clase principal de la aplicación gráfica.
    Hereda de tk.Tk y actúa como orquestador:
    - Crea el almacén de datos.
    - Instancia todas las vistas.
    - Conecta los callbacks entre módulos.
    """

    def __init__(self):
        super().__init__()
        self.title("🛒 Sistema de Gestión – Papelería")
        self.geometry("1100x680")
        self.resizable(True, True)
        self.configure(bg="#f0f4f8")

        self.almacen = Almacen()
        self.ui = Utilidades()

        self.crear_interfaz()

    # ── Interfaz principal ───────────────────────────────────────────────────

    def crear_interfaz(self):
        """Construye la ventana principal: barra, menú lateral y área de contenido."""
        # Barra de título
        barra = tk.Frame(self, bg="#1a237e", height=55)
        barra.pack(fill="x")
        tk.Label(barra, text="📚  PAPELERÍA – Sistema de Gestión",
                 font=("Segoe UI", 16, "bold"), bg="#1a237e", fg="white",
                 pady=12).pack(side="left", padx=20)

        # Contenedor principal
        contenedor = tk.Frame(self, bg="#f0f4f8")
        contenedor.pack(fill="both", expand=True)

        # Menú lateral
        menu = tk.Frame(contenedor, bg="#283593", width=200)
        menu.pack(side="left", fill="y")
        menu.pack_propagate(False)
        self._crear_menu_lateral(menu)

        # Notebook (pestañas ocultas; la navegación es por el menú lateral)
        self.notebook = ttk.Notebook(contenedor)
        self.notebook.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        style = ttk.Style()
        style.layout("TNotebook.Tab", [])   # oculta las pestañas visualmente

        self._construir_vistas()

    def _crear_menu_lateral(self, menu):
        tk.Label(menu, text="Menú", font=("Segoe UI", 12, "bold"),
                 bg="#283593", fg="#90caf9", pady=15).pack(fill="x")

        opciones = [
            ("🏠  Inicio",            0),
            ("📦  Productos",         1),
            ("🚚  Proveedores",       2),
            ("👥  Clientes",          3),
            ("🛒  Nueva Venta",       4),
            ("📋  Historial Ventas",  5),
        ]
        for texto, idx in opciones:
            tk.Button(
                menu, text=texto, font=("Segoe UI", 11),
                bg="#283593", fg="white", bd=0, padx=10, pady=12,
                activebackground="#3949ab", anchor="w", cursor="hand2",
                command=lambda i=idx: self.notebook.select(i)
            ).pack(fill="x")

        tk.Frame(menu, bg="#283593").pack(fill="both", expand=True)
        tk.Button(menu, text="❌  Salir", font=("Segoe UI", 11),
                  bg="#c62828", fg="white", bd=0, padx=10, pady=12,
                  activebackground="#b71c1c", cursor="hand2",
                  command=self.salir).pack(fill="x", side="bottom")

    def _construir_vistas(self):
        """Instancia cada vista y la agrega al notebook."""
        # ── Inicio ──
        self.frame_inicio = tk.Frame(self.notebook, bg="#f0f4f8")
        self.notebook.add(self.frame_inicio)
        self._construir_inicio()

        # ── Productos ──
        self.vista_productos = VistaProductos(
            self.notebook, self.almacen, self.ui
        )
        self.notebook.add(self.vista_productos)

        # ── Proveedores (callback → refresca combo en Productos) ──
        self.vista_proveedores = VistaProveedores(
            self.notebook, self.almacen, self.ui,
            callback_actualizar_combo=self.vista_productos.actualizar_combo_proveedores
        )
        self.notebook.add(self.vista_proveedores)

        # ── Ventas (se crea antes de Clientes para poder pasar el callback) ──
        self.vista_ventas = VistaVentas(
            self.notebook, self.almacen, self.ui,
            callback_post_venta=self._post_venta
        )
        self.notebook.add(self.vista_ventas)   # índice reservado para después de Clientes

        # ── Clientes (callback → refresca combo en Ventas) ──
        self.vista_clientes = VistaClientes(
            self.notebook, self.almacen, self.ui,
            callback_actualizar_combo=self.vista_ventas.actualizar_combo_clientes
        )
        self.notebook.add(self.vista_clientes)

        # ── Historial ──
        self.vista_historial = VistaHistorial(
            self.notebook, self.almacen, self.ui
        )
        self.notebook.add(self.vista_historial)

        # Reordenar tabs: Inicio(0) Productos(1) Proveedores(2) Clientes(3) Ventas(4) Historial(5)
        # El notebook los agrega en el orden en que se llama notebook.add(); ajustamos el orden
        # moviendo la pestaña de Ventas (actualmente en posición 3) a la posición 4.
        tabs = list(self.notebook.tabs())
        # tabs: [inicio, productos, proveedores, ventas, clientes, historial]
        # Queremos: [inicio, productos, proveedores, clientes, ventas, historial]
        # Borramos y re-añadimos en el orden correcto
        for tab in tabs:
            self.notebook.forget(tab)

        orden = [
            self.frame_inicio,
            self.vista_productos,
            self.vista_proveedores,
            self.vista_clientes,
            self.vista_ventas,
            self.vista_historial,
        ]
        for frame in orden:
            self.notebook.add(frame)

        self.notebook.select(0)

    # ── MÓDULO INICIO ────────────────────────────────────────────────────────

    def _construir_inicio(self):
        f = self.frame_inicio
        tk.Label(f, text="Bienvenido al Sistema de Papelería",
                 font=("Segoe UI", 20, "bold"), bg="#f0f4f8", fg="#1a237e").pack(pady=40)
        tk.Label(f, text="Selecciona una opción del menú lateral para comenzar.",
                 font=("Segoe UI", 13), bg="#f0f4f8", fg="#555").pack()

        fila = tk.Frame(f, bg="#f0f4f8")
        fila.pack(pady=30)

        tarjetas = [
            ("📦 Productos",  "#1565c0", lambda: len(self.almacen.productos)),
            ("🚚 Proveedores","#2e7d32", lambda: len(self.almacen.proveedores)),
            ("👥 Clientes",   "#6a1b9a", lambda: len(self.almacen.clientes)),
            ("🛒 Ventas",     "#e65100", lambda: len(self.almacen.ventas)),
        ]
        self._labels_tarjeta = []
        for titulo, color, fn in tarjetas:
            card = tk.Frame(fila, bg=color, width=180, height=100)
            card.pack(side="left", padx=12)
            card.pack_propagate(False)
            tk.Label(card, text=titulo, font=("Segoe UI", 12, "bold"),
                     bg=color, fg="white").pack(pady=(18, 4))
            lbl = tk.Label(card, text=str(fn()), font=("Segoe UI", 22, "bold"),
                           bg=color, fg="white")
            lbl.pack()
            self._labels_tarjeta.append((lbl, fn))

        tk.Button(f, text="🔄 Actualizar resumen", font=("Segoe UI", 10),
                  bg="#1a237e", fg="white", bd=0, padx=12, pady=6, cursor="hand2",
                  command=self._actualizar_tarjetas).pack(pady=10)

    def _actualizar_tarjetas(self):
        for lbl, fn in self._labels_tarjeta:
            lbl.config(text=str(fn()))

    # ── Callbacks entre módulos ──────────────────────────────────────────────

    def _post_venta(self):
        """
        Se ejecuta tras registrar una venta:
        actualiza la tabla de productos, el combo de ventas y las tarjetas de inicio.
        """
        self.vista_productos.consultar_productos()
        self.vista_ventas.actualizar_combo_productos()
        self.vista_historial.refrescar()
        self._actualizar_tarjetas()

    # ── Salir ────────────────────────────────────────────────────────────────

    def salir(self):
        """Confirma y cierra la aplicación."""
        if messagebox.askyesno("Salir", "¿Deseas cerrar la aplicación?"):
            self.destroy()


# ── Punto de entrada ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = AppPapeleria()
    app.mainloop()
