from tkinter import messagebox
from tkinter import ttk
import tkinter as tk

from dtos import ProveedorDTO
from vistas import VistaTabla  

class VistaProveedores(tk.Frame):
    """Frame que contiene todo el módulo de gestión de proveedores."""

    def __init__(self, parent, servicio, utilidades, callback_actualizar_combo=None):
        super().__init__(parent, bg="#f0f4f8")
        self.servicio_proveedores = servicio
        self.ui = utilidades
        self.proveedores_en_memoria = {} # Cambiamos a diccionario
        self.config(bg="#F5F5F0")
        self._construir()

    def _construir(self):
        self.ui.titulo_seccion(self, "🚚 Gestión de Proveedores")
        self._construir_formulario()
        self._construir_buscador()
        
        # Instanciamos tu clase personalizada
        self.tabla = VistaTabla(self)
        self.tabla.pack(fill="both", expand=True, padx=15, pady=5)
        self.tabla.construir(("ID", "Nombre", "Teléfono", "Correo", "Dirección"))
        self.tabla.vincular_evento("<<TreeviewSelect>>", self._seleccionar_fila)
        
        self._rellenar_tabla()

    def _construir_buscador(self):
        buscador_frame = tk.Frame(self, bg="#F5F5F0")
        buscador_frame.pack(fill="x", padx=15, pady=(0, 5))
        
        tk.Label(buscador_frame, text=" Buscar proveedor:", bg="#f0f4f8", font=("Segoe UI", 9, "bold")).pack(side="left")
        self.ent_buscador = tk.Entry(buscador_frame, width=40, font=("Segoe UI", 10))
        self.ent_buscador.pack(side="left", padx=10)
        self.ent_buscador.bind("<KeyRelease>", self._filtrar_tabla)

    def _construir_formulario(self):
        form = tk.LabelFrame(self, text="Datos del Proveedor",
                             font=("Segoe UI", 10, "bold"),
                             bg="#F5F5F0", fg="#000000", padx=10, pady=8)
        form.pack(fill="x", padx=15, pady=5)

        col = tk.Frame(form, bg="#F5F5F0")
        col.pack(side="left", padx=8)
        tk.Label(col, text="ID:", bg="#F5F5F0",
                 font=("Segoe UI", 9)).grid(row=0, column=0, sticky="e", pady=4, padx=4)
        self.ent_ID = tk.Entry(col, width=30, font=("Segoe UI", 10), state="readonly")
        self.ent_ID.grid(row=0, column=1, sticky="w", pady=4)

        campos = [("Nombre:", "ent_nombre"), ("Teléfono:", "ent_telefono"),
                  ("Correo:", "ent_correo"), ("Dirección:", "ent_direccion")]
        for i, (lbl, attr) in enumerate(campos):
            tk.Label(col, text=lbl, bg="#F5F5F0",
                     font=("Segoe UI", 9)).grid(row=i+1, column=0, sticky="e", pady=4, padx=4)
            ent = tk.Entry(col, width=30, font=("Segoe UI", 10))
            ent.grid(row=i+1, column=1, sticky="w", pady=4)
            setattr(self, attr, ent)

        btn_frame = tk.Frame(form, bg="#F5F5F0")
        btn_frame.pack(side="left", padx=16, anchor="n", pady=6)
        self.btn_registrar = self.ui.boton(btn_frame, "💾 Registrar Proveedor", "#2e7d32",
                      self.registrar_proveedor)
        self.btn_registrar.pack(fill="x", pady=3)
        self.btn_actualizar=self.ui.boton(btn_frame, "Actualizar", "#1565c0", self.actualizar_proveedor)
        self.btn_actualizar.pack(fill="x", pady=3)
        self.btn_eliminar = self.ui.boton(btn_frame, "Eliminar", "#c62828", self.eliminar_proveedor)
        self.btn_eliminar.pack(fill="x", pady=3)

        self.btn_limpiar = self.ui.boton(btn_frame, "🧹 Limpiar", "#546e7a",
                      self.limpiar_campos)
        self.btn_limpiar.pack(fill="x", pady=3)

    # ── Métodos de negocio ───────────────────────────────────────────────────

    def registrar_proveedor(self):
        if not self._validar_campos():
            return
        try:
            nuevo_proveedor_dto = self._leer_campos()
            self.servicio_proveedores.registrar_proveedor(nuevo_proveedor_dto)
            messagebox.showinfo("Éxito", f"Proveedor '{nuevo_proveedor_dto.nombre}' registrado correctamente.")
            self.limpiar_campos()
            self._rellenar_tabla()
        except ValueError as e:
            messagebox.showerror("Validación", str(e))
        except Exception as e:
            messagebox.showerror("Error del Sistema", str(e))
    
    def actualizar_proveedor(self):
        id_proveedor= self.tabla.obtener_id_seleccionado()
        if id_proveedor is None:
            messagebox.showwarning("Aviso", "Selecciona un proveedor de la tabla.")
            return
        if not self._validar_campos():
            return
        try:
            dto=self._leer_campos()
            self.servicio_proveedores.actualizar_proveedor(int(id_proveedor), dto)
            messagebox.showinfo("Éxito", "Proveedor actualizado correctamente.")
            self.limpiar_campos()
            self._rellenar_tabla()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def eliminar_proveedor(self):
        id_proveedor = self.tabla.obtener_id_seleccionado()
        if id_proveedor is None:
            messagebox.showwarning("Aviso", "Selecciona un proveedor de la tabla.")
            return
        valores = self.tabla.obtener_fila_seleccionada()
        nombre = str(valores[1])
        if messagebox.askyesno("Confirmar", f"¿Eliminar al proveedor '{nombre}'?\nEsta acción no se puede deshacer."):
            try:
                self.servicio_proveedores.eliminar_proveedor(int(id_proveedor))
                messagebox.showinfo("Eliminado", "Proveedor eliminado correctamente.")
                self.limpiar_campos()
                self._rellenar_tabla()
            except Exception as e:
                if "1451" in str(e):
                    messagebox.showerror(
                        "No se puede eliminar",
                        f"El proveedor '{nombre}' tiene productos asociados.\n"
                        "No es posible eliminarlo mientras tenga productos registrados."
                    )
                else:
                    messagebox.showerror("Error", f"No se pudo eliminar: {str(e)}")




    def limpiar_campos(self):
        self.btn_registrar.config(state="normal")  # Habilitamos el botón de registrar al limpiar campos
        self.ent_ID.config(state="normal")
        self.ent_ID.delete(0, tk.END)
        self.ent_ID.config(state="readonly")
        for attr in ["ent_nombre", "ent_telefono", "ent_correo", "ent_direccion"]:
            getattr(self, attr).delete(0, tk.END)

    # ── Auxiliares ───────────────────────────────────────────────────────────

    def _leer_campos(self) -> ProveedorDTO:
        return ProveedorDTO(
            nombre=self.ent_nombre.get().strip(),
            telefono=self.ent_telefono.get().strip(),
            correo=self.ent_correo.get().strip(),
            direccion=self.ent_direccion.get().strip(),
            id_proveedor=None
        )
        
    def _validar_campos(self):
        if not self.ent_nombre.get().strip():
            messagebox.showerror("Validación", "El nombre del proveedor es obligatorio.")
            return False
        if self.ent_telefono.get().strip() and not self.ent_telefono.get().strip().isdigit():
            messagebox.showerror("Validación", "El teléfono debe contener solo números.")
            return False
        return True
    
    def _rellenar_tabla(self):
        self.proveedores_en_memoria.clear()
            
        for p in self.servicio_proveedores.consultar_proveedores():
            # Llenamos el diccionario maestro
            self.proveedores_en_memoria[p.id_proveedor] = (p.id_proveedor, p.nombre, p.telefono, p.correo, p.direccion)
            
        self.tabla.actualizar_tabla(self.proveedores_en_memoria)

    def _filtrar_tabla(self, event):
        termino = self.ent_buscador.get().lower().strip()
        
        if not termino:
            self.tabla.actualizar_tabla(self.proveedores_en_memoria)
            return
            
        filtrados = {}
        for id_proveedor, valores in self.proveedores_en_memoria.items():
            if termino in " ".join(str(v).lower() for v in valores):
                filtrados[id_proveedor] = valores
                
        self.tabla.actualizar_tabla(filtrados)

    def _seleccionar_fila(self, event=None):
        # Usamos tu propio método encapsulado
        valores = self.tabla.obtener_fila_seleccionada()
        if not valores: 
            return
        
        self.limpiar_campos()
        self.btn_registrar.config(state="disabled")  # Deshabilitamos el botón de registrar al seleccionar una fila
        self.ent_nombre.insert(0, valores[1])
        self.ent_telefono.insert(0, valores[2] if valores[2] != "None" else "")
        self.ent_correo.insert(0, valores[3] if valores[3] != "None" else "")
        self.ent_direccion.insert(0, valores[4] if len(valores) > 4 and valores[4] != "None" else "")
    
    def refrescar_datos(self):
        self.limpiar_campos()
        self.ent_buscador.delete(0, tk.END)
        self._rellenar_tabla()