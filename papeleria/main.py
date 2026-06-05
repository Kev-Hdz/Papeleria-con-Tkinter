import tkinter as tk
from tkinter import SEL, ttk, messagebox

from config import obtener_config_db
from datos import ContactoRepositorio, ProductoRepositorio, VentaRepositorio
from servicios import ContactoServicio, ProductoServicio, VentaServicio
from vistas import Utilidades, VistaProductos, VistaProveedores, VistaClientes, VistaInicio, VistaVentas, VistaHistorial


class AppPapeleria(tk.Tk):
    """
    Clase principal de la aplicación gráfica. Orquesta la inicialización.
    """

    def __init__(self):
        super().__init__()
        self.title("🛒 Sistema de Gestión – Papelería")
        self.geometry("1100x680")
        self.resizable(True, True)
        self.configure(bg="#f0f4f8")
        
        # 1. Configuración de BD única
        db_config = obtener_config_db()
        
        # 2. Inicialización de Capasproducto_repositorio
        self.servicio_producto = ProductoServicio(ProductoRepositorio(db_config))
        self.servicio_contacto = ContactoServicio(ContactoRepositorio(db_config))
        self.servicio_ventas = VentaServicio(VentaRepositorio(db_config), ProductoRepositorio(db_config))  # Placeholder para futuras ventas
        self.ui = Utilidades()

        # 3. Construcción Gráfica
        self.crear_interfaz()

    def crear_interfaz(self):
        """Construye la ventana principal y los contenedores estructurales."""
        barra = tk.Frame(self, bg="#1a237e", height=55)
        barra.pack(fill="x")
        tk.Label(barra, text="📚  PAPELERÍA – Sistema de Gestión",
                 font=("Segoe UI", 16, "bold"), bg="#1a237e", fg="white",
                 pady=12).pack(side="left", padx=20)

        contenedor = tk.Frame(self, bg="#f0f4f8")
        contenedor.pack(fill="both", expand=True)

        menu = tk.Frame(contenedor, bg="#283593", width=200)
        menu.pack(side="left", fill="y")
        menu.pack_propagate(False)
        self._crear_menu_lateral(menu)

        self.notebook = ttk.Notebook(contenedor)
        self.notebook.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        style = ttk.Style()
        style.layout("TNotebook.Tab", [])  # Oculta las pestañas visuales
        self.notebook.bind("<<NotebookTabChanged>>", self._al_cambiar_pestana)
        self._construir_vistas()
        
    def _al_cambiar_pestana(self, event):
        """Evento que se dispara al cambiar de pestaña. Permite recargar datos si la vista lo requiere."""
        vista_actual = self.notebook.nametowidget(self.notebook.select())
        if hasattr(vista_actual, "refrescar_datos"):
            vista_actual.refrescar_datos()
            
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
        """Instancia cada vista y la agrega al notebook en el orden exacto del menú."""
        self.inicializar_vista_inicio()
        self.inicializar_vista_productos()
        self.inicializar_vista_proveedores()
        self.inicializar_vista_clientes()
        self.inicializar_vista_ventas()
        self.inicializar_vista_historial()
        self.notebook.select(0)
        
        # Índices 2 al 5: Placeholders temporales para evitar que el programa crashee
        

    def inicializar_vista_inicio(self):
        vista_inicio = VistaInicio(self.notebook, self.servicio_producto, self.servicio_contacto)
        self.notebook.add(vista_inicio)
    def inicializar_vista_productos(self):
        vista_productos = VistaProductos(self.notebook, self.servicio_producto, self.servicio_contacto, self.ui)
        self.notebook.add(vista_productos)
    def inicializar_vista_proveedores(self):
        vista_proveedores = VistaProveedores(self.notebook, self.servicio_contacto, self.ui)
        self.notebook.add(vista_proveedores)
    def inicializar_vista_clientes(self):
        vista_clientes = VistaClientes(self.notebook, self.servicio_contacto, self.ui)
        self.notebook.add(vista_clientes)
    def inicializar_vista_ventas(self):
         vista_ventas = VistaVentas(self.notebook, self.servicio_ventas,self.servicio_producto, self.servicio_contacto, self.ui)
         self.notebook.add(vista_ventas)
    def inicializar_vista_historial(self):
        vista_hist= VistaHistorial(self.notebook,self.servicio_ventas, self.ui)
        self.notebook.add(vista_hist)

        


    def salir(self):
        if messagebox.askyesno("Salir", "¿Deseas cerrar la aplicación?"):
            self.destroy()

if __name__ == "__main__":
    app = AppPapeleria()
    app.mainloop()