import tkinter as tk
from tkinter import ttk, messagebox

from vistas import VistaTabla
from dtos import VentaDTO, DetalleVentaDTO 

class VistaVentas(tk.Frame):
    """Módulo gráfico para procesar nuevas ventas (Punto de Venta)."""

    def __init__(self, parent, servicio_venta, servicio_producto, servicio_contacto, utilidades):
        super().__init__(parent, bg="#f0f4f8")
        self.servicio_venta = servicio_venta
        self.servicio_producto = servicio_producto
        self.servicio_contacto = servicio_contacto
        
        self.ui = utilidades
        
        # Carrito en memoria: Diccionario donde la llave es el nombre del producto 
        # y el valor es el objeto DetalleVentaDTO.
        self.carrito: dict[str, DetalleVentaDTO] = {}
        
        # Diccionarios de mapeo para ComboBoxes
        self.clientes_ids = {}
        self.productos_disp = {}
        
        self.total_venta = 0.0  
        
        self._cargar_datos()
        self._construir()

    def _cargar_datos(self):
        self.clientes_ids.clear()
        for c in self.servicio_contacto.consultar_clientes():
            self.clientes_ids[c.nombre] = c.id_cliente
            
        self.productos_disp.clear()
        for p in self.servicio_producto.consultar_productos():
            if p.existencia > 0: # Solo mostramos lo que tiene stock
                self.productos_disp[p.nombre] = {"id": p.id_producto, "precio": p.precio_venta, "existencia": p.existencia}
                
    def _construir(self):
        self.ui.titulo_seccion(self, "🛒 Punto de Venta (Nueva Venta)")
        self._construir_controles()
        
        # Tabla para el carrito de compras
        self.tabla_carrito = VistaTabla(self)
        self.tabla_carrito.pack(fill="both", expand=True, padx=15, pady=5)
        self.tabla_carrito.construir(("Producto", "Cantidad", "P. Unitario", "Subtotal"))

        self._construir_pie()

    def _construir_controles(self):
        form = tk.LabelFrame(self, text="Agregar Artículos", font=("Segoe UI", 10, "bold"),
                             bg="#f0f4f8", fg="#1a237e", padx=10, pady=10)
        form.pack(fill="x", padx=15, pady=5)

        tk.Label(form, text="Cliente:", bg="#f0f4f8").grid(row=0, column=0, sticky="e", padx=5)
        self.combo_cliente = ttk.Combobox(form, width=30, state="readonly")
        self.combo_cliente.grid(row=0, column=1, sticky="w", padx=5)
        self.combo_cliente["values"] = list(self.clientes_ids.keys())
        
        tk.Label(form, text="Producto:", bg="#f0f4f8").grid(row=0, column=2, sticky="e", padx=5)
        self.combo_producto = ttk.Combobox(form, width=30, state="readonly")
        self.combo_producto.grid(row=0, column=3, sticky="w", padx=5)
        self.combo_producto["values"] = list(self.productos_disp.keys())
        
        tk.Label(form, text="Cantidad:", bg="#f0f4f8").grid(row=0, column=4, sticky="e", padx=5)
        self.ent_cantidad = tk.Entry(form, width=8)
        self.ent_cantidad.insert(0, "1")
        self.ent_cantidad.grid(row=0, column=5, sticky="w", padx=5)

        self.ui.boton(form, "➕ Agregar al Carrito", "#0277bd", self.agregar_al_carrito).grid(row=0, column=6, padx=15)

    def _construir_pie(self):
        pie = tk.Frame(self, bg="#f0f4f8")
        pie.pack(fill="x", padx=15, pady=10)
        
        self.lbl_total = tk.Label(pie, text="Total: $0.00", font=("Segoe UI", 18, "bold"), bg="#f0f4f8", fg="#c62828")
        self.lbl_total.pack(side="left", padx=10)
        
        self.ui.boton(pie, "✅ Procesar Venta", "#2e7d32", self.procesar_venta).pack(side="right", padx=5)
        self.ui.boton(pie, "🗑️ Vaciar Carrito", "#d32f2f", self.vaciar_carrito).pack(side="right", padx=5)

    # ── Lógica de Interfaz ───────────────────────────────────────────────────

    def agregar_al_carrito(self):
        producto_nombre = self.combo_producto.get()
        if not producto_nombre:
            messagebox.showwarning("Aviso", "Selecciona un producto.")
            return
            
        try:
            cantidad = int(self.ent_cantidad.get())
            if cantidad <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un entero mayor a cero.")
            return

        datos_prod = self.productos_disp[producto_nombre]
        subtotal = cantidad * datos_prod["precio"]
        
        if producto_nombre in self.carrito:
            # Si ya está en el carrito, actualizamos el DTO existente
            item_dto = self.carrito[producto_nombre]
            item_dto.cantidad += cantidad
            item_dto.subtotal += subtotal
            
            self.tabla_carrito.actualizar_fila(item_dto.id_producto, (
                item_dto.nombre_producto, item_dto.cantidad, 
                f"${item_dto.precio_unitario:.2f}", f"${item_dto.subtotal:.2f}"
            ))
        else:
            # Si es nuevo, instanciamos el DTO
            item_dto = DetalleVentaDTO(
                id_producto=datos_prod["id"],
                nombre_producto=producto_nombre,
                cantidad=cantidad,
                precio_unitario=datos_prod["precio"],
                subtotal=subtotal
            )
            self.carrito[producto_nombre] = item_dto
            
            # Reflejamos en la UI
            self.tabla_carrito.agregar_fila(item_dto.id_producto, (
                item_dto.nombre_producto, item_dto.cantidad, 
                f"${item_dto.precio_unitario:.2f}", f"${item_dto.subtotal:.2f}"
            ))
            
        self.cacular_total()
        self.ent_cantidad.delete(0, tk.END)
        self.ent_cantidad.insert(0, "1")
    
    def cacular_total(self):
        # Ahora accedemos al atributo .subtotal del DTO
        self.total_venta = sum(item_dto.subtotal for item_dto in self.carrito.values())
        self.lbl_total.config(text=f"Total: ${self.total_venta:.2f}")
        
    def vaciar_carrito(self):
        if messagebox.askyesno("Confirmar", "¿Deseas vaciar el carrito?"):
            self.carrito.clear()
            self.tabla_carrito.limpiar_tabla()
            self.total_venta = 0.0
            self.lbl_total.config(text="Total: $0.00")

    def refrescar_datos(self):
        self.tabla_carrito.limpiar_tabla()
        self._cargar_datos()
        self.combo_cliente.set("")
        self.combo_producto.set("")
        self.combo_cliente["values"] = list(self.clientes_ids.keys())

        self.combo_producto["values"] = list(self.productos_disp.keys())
        self.ent_cantidad.delete(0, tk.END)
        self.ent_cantidad.insert(0, "1")
        self.carrito.clear()
        self.total_venta = 0.0
        self.lbl_total.config(text="Total: $0.00")
    
    def procesar_venta(self):
        if not self.carrito:
            messagebox.showwarning("Aviso", "El carrito está vacío.")
            return
            
        cliente_nombre = self.combo_cliente.get()
        if not cliente_nombre:
            messagebox.showwarning("Aviso", "Selecciona un cliente.")
            return

        id_cliente = self.clientes_ids[cliente_nombre]
        
        # 1. Empaquetamos la cabecera y los detalles en un solo VentaDTO
        nueva_venta_dto = VentaDTO(
            id_cliente=id_cliente,
            total=self.total_venta,
            detalles=list(self.carrito.values())
        )

        try:
            # 2. Enviamos el objeto estandarizado al servicio
            self.servicio_venta.registrar_nueva_venta(nueva_venta_dto)
            messagebox.showinfo("Éxito", "Venta procesada y guardada correctamente.")
            self.refrescar_datos() 
            
        except ValueError as e:
            # Atrapamos errores de negocio (ej. Falta de stock, cantidades inválidas)
            messagebox.showwarning("Aviso de Inventario", str(e))
        except Exception as e:
            # Atrapamos errores críticos (ej. Caída de base de datos o sintaxis SQL)
            messagebox.showerror("Error del Sistema", f"Ocurrió un error inesperado al procesar la venta:\n{str(e)}")