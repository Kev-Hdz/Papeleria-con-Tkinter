import tkinter as tk
from tkinter import ttk

from vistas import utilidades

class VistaTabla(tk.Frame):
    """Vista genérica para mostrar tablas de datos con título y estilo uniforme."""

    def __init__(self, parent):
        super().__init__(parent, bg="#f0f4f8")
        
        self.pack(fill="both", expand=True)

        self.tabla = None
        
        self._configurar_estilos()
    def _configurar_estilos(self):
        style = ttk.Style()
        style.configure("Treeview", font=("Segoe UI", 9), rowheight=24,
                         background="white", fieldbackground="white")
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"),
                         background="#1a237e", foreground="white")
        style.map("Treeview", background=[("selected", "#3949ab")])
    def construir(self, columnas, height=8):
        """Construye la tabla con las columnas especificadas."""
        sb = ttk.Scrollbar(self, orient="vertical")
        sb.pack(side="right", fill="y")

        self.tabla = ttk.Treeview(self, columns=columnas, show="headings",
                              height=height, yscrollcommand=sb.set)
        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, anchor="center", width=110)
        self.tabla.pack(fill="both", expand=True)
        sb.config(command=self.tabla.yview)

    def obtener_fila_seleccionada(self):
        """Retorna los datos de la fila actualmente seleccionada o None si no hay selección."""
        seleccion = self.tabla.selection()
        if seleccion:
            return self.tabla.item(seleccion[0])["values"]
        return None
    def obtener_id_seleccionado(self):
        """Retorna el ID (iid) de la fila actualmente seleccionada o None si no hay selección."""
        seleccion = self.tabla.selection()
        if seleccion:
            print("ID seleccionado:", seleccion[0])
            print(type(seleccion[0]))
            return seleccion[0] 
        return None
    def agregar_fila(self, id, datos):
        """Agrega una fila a la tabla. 'datos' debe ser una tupla con el mismo orden que las columnas."""
        self.tabla.insert("", "end", iid=id, values=datos)
    
    def actualizar_fila(self, item_id, datos):
        """Actualiza una fila existente identificada por 'item_id' con nuevos 'datos'."""
        self.tabla.item(item_id, values=datos)
    
    def eliminar_fila(self, item_id):
        """Elimina una fila de la tabla identificada por 'item_id'."""
        self.tabla.delete(item_id)
    
    def actualizar_tabla(self, dict_datos):
        """Reemplaza todo el contenido de la tabla con 'dict_datos', que debe ser un diccionario donde las claves son los IDs y los valores son las tuplas de datos."""
        self.limpiar_tabla()
        for id, datos in dict_datos.items():
            self.agregar_fila(id, datos)
    
    def limpiar_tabla(self):
        """Elimina todas las filas de la tabla."""
        for row in self.tabla.get_children():
            self.tabla.delete(row)
    
    def vincular_evento(self, evento, callback):
        """Permite enlazar eventos directamente al Treeview interno."""
        if self.tabla:
            self.tabla.bind(evento, callback)

