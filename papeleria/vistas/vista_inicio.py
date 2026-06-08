import tkinter as tk

class VistaInicio(tk.Frame):
    """Pantalla principal (Dashboard) de la aplicación."""
    
    def __init__(self, parent, servicio_producto, servicio_contacto):
        super().__init__(parent, bg="#f0f4f8")
        self.servicio_producto = servicio_producto
        self.servicio_contacto = servicio_contacto
        self._labels_tarjeta = []
        self.config(bg="#F5F5F0")
        self._construir()

    def _construir(self):
        tk.Label(self, text="Bienvenido al Sistema de Papelería",
                 font=("Segoe UI", 20, "bold"), bg="#f0f4f8", fg="#000000").pack(pady=40)
        tk.Label(self, text="Selecciona una opción del menú lateral para comenzar.",
                 font=("Segoe UI", 13), bg="#F5F5F0", fg="#000000").pack()

        fila = tk.Frame(self, bg="#F5F5F0")
        fila.pack(pady=30)

        # Configuramos los datos de las tarjetas
        tarjetas = [
            ("📦 Productos",  "#1565c0", lambda: len(self.servicio_producto.consultar_productos())),
            ("🚚 Proveedores","#2e7d32", lambda: len(self.servicio_contacto.consultar_proveedores())),
            ("👥 Clientes",   "#6a1b9a", lambda: len(self.servicio_contacto.consultar_clientes())),
        ]
        
        for titulo, color, fn in tarjetas:
            card = tk.Frame(fila, bg=color, width=180, height=100)
            card.pack(side="left", padx=12)
            card.pack_propagate(False)
            tk.Label(card, text=titulo, font=("Segoe UI", 12, "bold"),
                     bg=color, fg="white").pack(pady=(18, 4))
            
            # Llamamos a la función segura para obtener el número actual
            lbl = tk.Label(card, text=self._obtener_conteo_seguro(fn), font=("Segoe UI", 22, "bold"),
                           bg=color, fg="white")
            lbl.pack()
            self._labels_tarjeta.append((lbl, fn))

        tk.Button(self, text="🔄 Actualizar resumen", font=("Segoe UI", 10),
                  bg="#e07b39", fg="white", bd=0, padx=12, pady=6, cursor="hand2",
                  command=self.actualizar_tarjetas).pack(pady=10)

    def _obtener_conteo_seguro(self, func_conteo):
        """Evita que un error en la BD rompa la interfaz de inicio."""
        try:
            return str(func_conteo())
        except Exception:
            return "0"

    def actualizar_tarjetas(self):
        for lbl, fn in self._labels_tarjeta:
            lbl.config(text=self._obtener_conteo_seguro(fn))