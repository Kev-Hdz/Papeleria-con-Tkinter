"""
Utilidades de interfaz gráfica.
Contiene métodos auxiliares reutilizables por todas las vistas:
creación de tablas, botones, títulos de sección y validación genérica.
"""

import tkinter as tk
from tkinter import ttk


class Utilidades:
    """
    Proporciona métodos de construcción de widgets compartidos
    entre todas las vistas de la aplicación.
    """

    @staticmethod
    def titulo_seccion(parent, texto):
        """Muestra un título de sección con línea divisoria azul."""
        tk.Label(parent, text=texto, font=("Segoe UI", 14, "bold"),
                 bg="#F5F5F0", fg="#000000", pady=8).pack(anchor="w", padx=15)
        tk.Frame(parent, bg="#F5F5F0", height=2).pack(fill="x", padx=15, pady=(0, 6))

    @staticmethod
    def boton(parent, texto, color, comando):
        """Crea y retorna un botón con estilo uniforme."""
        return tk.Button(
            parent, text=texto, font=("Segoe UI", 9, "bold"),
            bg=color, fg="white", bd=0, padx=10, pady=5,
            activebackground=color, cursor="hand2", command=comando
        )

    @staticmethod
    def crear_tabla(parent, columnas, height=8):
        """
        Crea un Treeview con scrollbar vertical dentro de un Frame contenedor.
        Retorna el widget Treeview listo para usar.
        """
        
        frame = tk.Frame(parent, bg="#F5F5F0")
        frame.pack(fill="both", expand=True, padx=15, pady=4)

        style = ttk.Style()
        style.theme_use("clam")
        style.layout("TNotebook.Tab",[])
        style.configure("TNotebook", tabmargins=[0,0,0,0])
        style.configure("Treeview", font=("Segoe UI", 9), rowheight=24,
                         background="white", fieldbackground="white")
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"),
                         background="#1a237e", foreground="white")
        style.map("Treeview.Heading", background=[("active", "#1a237e")], foreground=[("active", "white")])

        sb = ttk.Scrollbar(frame, orient="vertical")
        sb.pack(side="right", fill="y")

        tabla = ttk.Treeview(frame, columns=columnas, show="headings",
                              height=height, yscrollcommand=sb.set)
        for col in columnas:
            tabla.heading(col, text=col)
            tabla.column(col, anchor="center", width=110)
        tabla.pack(fill="both", expand=True)
        sb.config(command=tabla.yview)
        return tabla

    @staticmethod
    def validar_datos(valor, tipo="texto"):
        """
        Valida un valor según el tipo indicado.
        Tipos soportados: 'texto', 'numerico', 'entero'.
        Retorna True si el dato es válido, False en caso contrario.
        """
        if tipo == "texto":
            return bool(str(valor).strip())
        if tipo == "numerico":
            try:
                return float(valor) > 0
            except (ValueError, TypeError):
                return False
        if tipo == "entero":
            try:
                return int(valor) >= 0
            except (ValueError, TypeError):
                return False
        return False
