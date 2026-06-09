import tkinter as tk
from tkinter import ttk, messagebox
from servicios import ProductoServicio, ContactoServicio
from vistas.vista_tabla import VistaTabla
from dtos import ProductoDTO  # Importación necesaria para enviar datos al servicio

class VistaProductos(tk.Frame):
    """Frame que contiene todo el módulo de gestión de productos."""

    def __init__(self, parent, servicio_producto: ProductoServicio, servicio_contacto: ContactoServicio, utilidades):
        super().__init__(parent, bg="#f0f4f8")
        self.servicio_producto = servicio_producto
        self.servicio_contacto = servicio_contacto
        self.ui = utilidades 
        
        self.proveedores_ids = {}
        self.categorias_ids = {}
        self.marcas_ids = {}
        self.config(bg="#F5F5F0")
        # Diccionario maestro para el buscador local
        self.productos_en_memoria = {}
        self.config(relief="solid",bd=1)
        self._cargar_datos()
        self._construir()
        
    def _cargar_datos(self):
        """Carga los mapeos de IDs necesarios para los ComboBoxes."""
        self.proveedores_ids.clear()
        self.categorias_ids.clear()
        self.marcas_ids.clear()

        for p in self.servicio_contacto.consultar_proveedores():
            self.proveedores_ids[p.nombre] = p.id_proveedor
            
        for c in self.servicio_producto.consultar_categorias():
            self.categorias_ids[c["nombre_categoria"]] = c["id_categoria"]
            
        for m in self.servicio_producto.consultar_marcas():
            self.marcas_ids[m["nombre_marca"]] = m["id_marca"]

    def refrescar_datos(self):
        """Callback que se llama al entrar a la pestaña para actualizar combos y tabla."""
        self._limpiar_campos()
        self.ent_buscador.delete(0, tk.END)
        self._cargar_datos()
        
        # Actualizamos las opciones de los Combobox con los datos frescos
        self.combo_categoria["values"] = list(self.categorias_ids.keys())
        self.combo_proveedor["values"] = list(self.proveedores_ids.keys())
        self.combo_marca["values"] = list(self.marcas_ids.keys())
        
        self.consultar_productos()

    def _construir(self):
        self.ui.titulo_seccion(self, "📦 Gestión de Productos")
        self._construir_formulario()
        self._construir_buscador() # Nuevo módulo
        
        self.tabla = VistaTabla(self)
        self.tabla.pack(fill="both", expand=True, padx=15, pady=5)
        self.tabla.construir(("ID", "Nombre", "Categoría", "Marca", "P.Compra",
                             "P.Venta", "Existencia", "Proveedor", "Fecha Registro", "Descripción"))
        self.tabla.vincular_evento("<<TreeviewSelect>>", self._seleccionar_fila)
        self.consultar_productos()

    def _construir_buscador(self):
        """Crea la barra de búsqueda universal encima de la tabla."""
        buscador_frame = tk.Frame(self, bg="#f0f4f8")
        buscador_frame.pack(fill="x", padx=15, pady=(5, 0))
        
        tk.Label(buscador_frame, text="🔍 Buscar en tabla:", bg="#F5F5F0", font=("Segoe UI", 9, "bold")).pack(side="left")
        self.ent_buscador = tk.Entry(buscador_frame, width=50, font=("Segoe UI", 10))
        self.ent_buscador.pack(side="left", padx=10)
        
        # Evento que se dispara cada vez que el usuario suelta una tecla
        self.ent_buscador.bind("<KeyRelease>", self._filtrar_tabla_local)

    # ... [_construir_formulario queda exactamente igual a tu código] ...
    def _construir_formulario(self):
        form = tk.LabelFrame(self, text="Datos del Producto", font=("Segoe UI", 10, "bold"), bg="#F5F5F0", fg="#000000", padx=10, pady=8)
        form.pack(fill="x", padx=15, pady=(5, 3))

        col_izq = tk.Frame(form, bg="#F5F5F0")
        col_izq.pack(side="left", padx=8)
        campos = [("ID:", "ent_ID"),("Nombre:", "ent_nombre"), ("Precio Compra $:", "ent_precio_compra"),
                  ("Precio Venta $:", "ent_precio_venta"), ("Existencia:", "ent_existencia")]
        
        for i, (lbl, attr) in enumerate(campos):
            tk.Label(col_izq, text=lbl, bg="#F5F5F0", font=("Segoe UI", 9)).grid(row=i, column=0, sticky="e", pady=3, padx=4)
            ent = tk.Entry(col_izq, width=22, font=("Segoe UI", 10))
            if attr == "ent_ID":
                ent.config(state="readonly")
            ent.grid(row=i, column=1, sticky="w", pady=3)
            setattr(self, attr, ent)

        col_der = tk.Frame(form, bg="#F5F5F0")
        col_der.pack(side="left", padx=8)

        tk.Label(col_der, text="Categoría:", bg="#F5F5F0", font=("Segoe UI", 9)).grid(row=0, column=0, sticky="e", pady=3, padx=4)
        self.combo_categoria = ttk.Combobox(col_der, width=20, state="readonly", font=("Segoe UI", 10))
        self.combo_categoria["values"] = list(self.categorias_ids.keys())
        self.combo_categoria.grid(row=0, column=1, sticky="w", pady=3)

        tk.Label(col_der, text="Proveedor:", bg="#F5F5F0", font=("Segoe UI", 9)).grid(row=1, column=0, sticky="e", pady=3, padx=4)
        self.combo_proveedor = ttk.Combobox(col_der, width=20, state="readonly", font=("Segoe UI", 10))
        self.combo_proveedor["values"] = list(self.proveedores_ids.keys())
        self.combo_proveedor.grid(row=1, column=1, sticky="w", pady=3)

        tk.Label(col_der, text="Marca:", bg="#F5F5F0", font=("Segoe UI", 9)).grid(row=2, column=0, sticky="e", pady=3, padx=4)
        self.combo_marca = ttk.Combobox(col_der, width=20, state="readonly", font=("Segoe UI", 10))
        self.combo_marca["values"] = list(self.marcas_ids.keys())
        self.combo_marca.grid(row=2, column=1, sticky="w", pady=3)

        tk.Label(col_der, text="Descripción:", bg="#F5F5F0", font=("Segoe UI", 9)).grid(row=3, column=0, sticky="ne", pady=3, padx=4)
        self.txt_descripcion = tk.Text(col_der, width=22, height=3, font=("Segoe UI", 10))
        self.txt_descripcion.grid(row=3, column=1, rowspan=2, sticky="w", pady=3)

        btn_frame = tk.Frame(form, bg="#f0f4f8")
        btn_frame.pack(side="left", padx=16, anchor="n", pady=6)
        self.ui.boton(btn_frame, "💾 Registrar",  "#2e7d32", self.registrar_producto).pack(fill="x", pady=3)
        self.ui.boton(btn_frame, "✏️ Actualizar", "#1565c0", self.actualizar_producto).pack(fill="x", pady=3)
        self.ui.boton(btn_frame, "🗑️ Eliminar",   "#c62828", self.eliminar_producto).pack(fill="x", pady=3)
        self.ui.boton(btn_frame, "🧹 Limpiar",    "#546e7a", self._limpiar_campos).pack(fill="x", pady=3)


    # ── Lógica Central ───────────────────────────────────────────────────────

    def consultar_productos(self):
        """Carga los productos de la BD, los guarda en memoria y llena la tabla."""
        self.productos_en_memoria.clear()
        
        for p in self.servicio_producto.consultar_productos():
            # El orden debe coincidir exactamente con el construir() de VistaTabla
            self.productos_en_memoria[p.id_producto] = (
                p.id_producto, p.nombre, p.nombre_categoria, p.nombre_marca,
                f"{p.precio_compra:.2f}", f"{p.precio_venta:.2f}",
                p.existencia, p.nombre_proveedor, p.fecha_registro, p.descripcion
            )
            
        self.tabla.actualizar_tabla(self.productos_en_memoria)

    def _filtrar_tabla_local(self, event):
        """Se activa al escribir. Filtra los datos maestros y redibuja la tabla."""
        termino = self.ent_buscador.get().lower().strip()
        
        # Si el buscador está vacío, mostramos todos los productos de nuevo
        if not termino:
            self.tabla.actualizar_tabla(self.productos_en_memoria)
            return
            
        productos_filtrados = {}
        for id_prod, valores_fila in self.productos_en_memoria.items():
            # Convertimos toda la fila a un gran texto en minúsculas
            fila_texto = " ".join(str(v).lower() for v in valores_fila)
            
            # Si lo que escribimos está en alguna parte de ese texto, lo mostramos
            if termino in fila_texto:
                productos_filtrados[id_prod] = valores_fila
                
        self.tabla.actualizar_tabla(productos_filtrados)

    def registrar_producto(self):
        if not self._validar_campos():
            return
        try:
            nuevo_producto_dto = self._leer_campos()
            self.servicio_producto.registrar_producto(nuevo_producto_dto)
            messagebox.showinfo("Éxito", f"Producto '{nuevo_producto_dto.nombre}' registrado correctamente.")
            self._limpiar_campos()
            self.consultar_productos()
        except ValueError:
            messagebox.showerror("Error de Formato", "Los precios y existencias deben ser números válidos.")
        except Exception as e:
            messagebox.showerror("Validación", str(e))

    def actualizar_producto(self):
        id_producto = self.tabla.obtener_id_seleccionado()
        if id_producto is None:
            messagebox.showwarning("Aviso", "Selecciona un producto de la tabla.")
            return
        if not self._validar_campos():  
            return
        try:    
            producto_dto = self._leer_campos()
            self.servicio_producto.actualizar_producto(id_producto, producto_dto)
            messagebox.showinfo("Éxito", "Producto actualizado correctamente.")
            self._limpiar_campos()
            self.consultar_productos()
        except ValueError:
            messagebox.showerror("Error de Formato", "Los precios y existencias deben ser números válidos.")
        except Exception as e:
            messagebox.showerror("Validación", str(e))

    def eliminar_producto(self):
        id_producto = self.tabla.obtener_id_seleccionado()
        if id_producto is None:
            messagebox.showwarning("Aviso", "Selecciona un producto de la tabla.")
            return

        valores = self.tabla.obtener_fila_seleccionada()
        if not valores:
            return
        
        nombre_producto = str(valores[1]) # Corregido: Era texto, no int
        
        if messagebox.askyesno("Confirmar", f"¿Eliminar el producto '{nombre_producto}'?\nEsta acción no se puede deshacer."):
            try:
                self.servicio_producto.eliminar_producto(id_producto)
                messagebox.showinfo("Eliminado", "Producto eliminado correctamente.")
                self._limpiar_campos()
                self.consultar_productos()
            except Exception as e:
                if "1451" in str(e):
                    messagebox.showerror("No se puede eliminar", f"El producto {nombre_producto} tiene ventas registradas.\n"
                                         "No es posible eliminarlo para conservar el historial")
                else:
                    messagebox.showerror("Error", f"No se puede eliminar: {str(e)}")



                

    def _leer_campos(self) -> ProductoDTO:
        """Extrae los valores de la UI y los empaqueta en un ProductoDTO."""
        return ProductoDTO(
            nombre=self.ent_nombre.get().strip(),
            id_categoria=self.categorias_ids.get(self.combo_categoria.get()),
            id_marca=self.marcas_ids.get(self.combo_marca.get()),
            descripcion=self.txt_descripcion.get("1.0", tk.END).strip(),
            precio_compra=float(self.ent_precio_compra.get()),
            precio_venta=float(self.ent_precio_venta.get()),
            existencia=int(self.ent_existencia.get()),
            id_proveedor=self.proveedores_ids.get(self.combo_proveedor.get()),
            fecha_registro=None # El servicio lo asocia si es nuevo
        )

    # ... [_limpiar_campos, _validar_campos y _seleccionar_fila quedan igual] ...
    def _limpiar_campos(self):
        for attr in ["ent_ID","ent_nombre", "ent_precio_compra", "ent_precio_venta", "ent_existencia"]:
            getattr(self, attr).delete(0, tk.END)
        self.txt_descripcion.delete("1.0", tk.END)
        self.combo_categoria.set("")
        self.combo_proveedor.set("")
        self.combo_marca.set("")

    def _validar_campos(self) -> bool:
        if not self.ent_nombre.get().strip():
            messagebox.showerror("Validación", "El nombre del producto es obligatorio.")
            return False
        if not self.combo_categoria.get():
            messagebox.showerror("Validación", "Debes seleccionar una categoría.")
            return False
        if not self.combo_marca.get():
            messagebox.showerror("Validación", "Debes seleccionar una marca.")
            return False
        return True

    def _seleccionar_fila(self, event):
        valores = self.tabla.obtener_fila_seleccionada()
        
        if not valores:
            return
        
        # Limpiamos e insertamos
        self.ent_ID.delete(0,tk.END)
        self.ent_ID.insert(0,valores[0])
        self.ent_nombre.delete(0, tk.END)
        self.ent_nombre.insert(0, valores[1])
        
        self.combo_categoria.set(valores[2])
        self.combo_marca.set(valores[3])
        self.combo_proveedor.set(valores[7])
        
        self.ent_precio_compra.delete(0, tk.END)
        self.ent_precio_compra.insert(0, valores[4])
        self.ent_precio_venta.delete(0, tk.END)
        self.ent_precio_venta.insert(0, valores[5])
        
        self.ent_existencia.delete(0, tk.END)
        self.ent_existencia.insert(0, valores[6])
        
        self.txt_descripcion.delete("1.0", tk.END)
        self.txt_descripcion.insert("1.0", valores[9])