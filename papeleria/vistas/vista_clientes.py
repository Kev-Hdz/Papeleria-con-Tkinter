import tkinter as tk
from tkinter import messagebox

from dtos import ClienteDTO
from vistas import VistaTabla  
class VistaClientes(tk.Frame):
    """Frame que contiene todo el módulo de gestión de clientes."""

    def __init__(self, parent, servicio, utilidades, callback_actualizar_combo=None):
        super().__init__(parent, bg="#f0f4f8")
        self.servicio_cliente = servicio
        self.ui = utilidades
        # Cambiamos a diccionario para ser compatibles con VistaTabla
        self.clientes_en_memoria = {} 
        self._construir()

    def _construir(self):
        self.ui.titulo_seccion(self, "👥 Gestión de Clientes")
        self._construir_formulario()
        self._construir_buscador()
        
        # Instanciamos tu clase personalizada
        self.tabla = VistaTabla(self)
        self.tabla.pack(fill="both", expand=True, padx=15, pady=5)
        self.tabla.construir(("ID", "Nombre", "Teléfono", "Correo"))
        self.tabla.vincular_evento("<<TreeviewSelect>>", self._seleccionar_fila)
        
        self._rellenar_tabla()

    def _construir_buscador(self):
        buscador_frame = tk.Frame(self, bg="#f0f4f8")
        buscador_frame.pack(fill="x", padx=15, pady=(0, 5))
        
        tk.Label(buscador_frame, text="🔍 Buscar cliente:", bg="#f0f4f8", font=("Segoe UI", 9, "bold")).pack(side="left")
        self.ent_buscador = tk.Entry(buscador_frame, width=40, font=("Segoe UI", 10))
        self.ent_buscador.pack(side="left", padx=10)
        self.ent_buscador.bind("<KeyRelease>", self._filtrar_tabla)

    def _construir_formulario(self):
        form = tk.LabelFrame(self, text="Datos del Cliente",
                             font=("Segoe UI", 10, "bold"),
                             bg="#f0f4f8", fg="#1a237e", padx=10, pady=8)
        form.pack(fill="x", padx=15, pady=5)

        col = tk.Frame(form, bg="#f0f4f8")
        col.pack(side="left", padx=8)
        campos = [("Nombre:", "ent_nombre"),
                  ("Teléfono:", "ent_telefono"),
                  ("Correo:", "ent_correo")]
        for i, (lbl, attr) in enumerate(campos):
            tk.Label(col, text=lbl, bg="#f0f4f8",
                     font=("Segoe UI", 9)).grid(row=i, column=0, sticky="e", pady=4, padx=4)
            ent = tk.Entry(col, width=30, font=("Segoe UI", 10))
            ent.grid(row=i, column=1, sticky="w", pady=4)
            setattr(self, attr, ent)

        btn_frame = tk.Frame(form, bg="#f0f4f8")
        btn_frame.pack(side="left", padx=16, anchor="n", pady=6)
        self.ui.boton(btn_frame, "💾 Registrar Cliente", "#2e7d32",
                      self.registrar_cliente).pack(fill="x", pady=3)
        self.ui.boton(btn_frame, "🧹 Limpiar", "#546e7a",
                      self.limpiar_campos).pack(fill="x", pady=3)

    # ── Métodos de negocio ───────────────────────────────────────────────────

    def registrar_cliente(self):
        if not self._validar_campos():
            return
        try:
            nuevo_cliente_dto = self._leer_campos()
            self.servicio_cliente.registrar_cliente(nuevo_cliente_dto)
            messagebox.showinfo("Éxito", f"Cliente '{nuevo_cliente_dto.nombre}' registrado correctamente.")
            self.limpiar_campos()
            self._rellenar_tabla() 
        except Exception as e:
            messagebox.showerror("Error del Sistema", str(e))

    def limpiar_campos(self):
        for attr in ["ent_nombre", "ent_telefono", "ent_correo"]:
            getattr(self, attr).delete(0, tk.END)

    # ── Auxiliares ───────────────────────────────────────────────────────────

    def _leer_campos(self) -> ClienteDTO:
        return ClienteDTO(
            nombre=self.ent_nombre.get().strip(),
            telefono=self.ent_telefono.get().strip(),
            correo=self.ent_correo.get().strip(),
            id_cliente=None
        )
        
    def _validar_campos(self):
        if not self.ent_nombre.get().strip():
            messagebox.showerror("Validación", "El nombre del cliente es obligatorio.")
            return False
        if self.ent_telefono.get().strip() and not self.ent_telefono.get().strip().isdigit():
            messagebox.showerror("Validación", "El teléfono debe contener solo números.")
            return False
        return True

    def _rellenar_tabla(self):
        self.clientes_en_memoria.clear()
        
        for c in self.servicio_cliente.consultar_clientes():
            # Llenamos el diccionario con el formato esperado por VistaTabla
            self.clientes_en_memoria[c.id_cliente] = (c.id_cliente, c.nombre, c.telefono, c.correo)
             
        self.tabla.actualizar_tabla(self.clientes_en_memoria)

    def _filtrar_tabla(self, event):
        termino = self.ent_buscador.get().lower().strip()
        
        if not termino:
            self.tabla.actualizar_tabla(self.clientes_en_memoria)
            return
            
        filtrados = {}
        for id_cliente, valores in self.clientes_en_memoria.items():
            if termino in " ".join(str(v).lower() for v in valores):
                filtrados[id_cliente] = valores
                
        self.tabla.actualizar_tabla(filtrados)

    def _seleccionar_fila(self, event):
        # Usamos tu propio método encapsulado
        valores = self.tabla.obtener_fila_seleccionada()
        if not valores: 
            return
        
        self.limpiar_campos()
        self.ent_nombre.insert(0, valores[1])
        self.ent_telefono.insert(0, valores[2] if valores[2] != "None" else "")
        self.ent_correo.insert(0, valores[3] if valores[3] != "None" else "")