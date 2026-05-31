from datetime import datetime

class ProductoPapeleria:
    """
    Representa un artículo que se vende en la papelería.
    
    Args:
        
    
    Raises:
        ValueError: Si los precios son negativos o si la existencia es negativa.
    """

    def __init__(self, id: int, nombre: str, id_categoria: int, id_marca: int, descripcion: str,
                 precio_compra: float, precio_venta: float, existencia: int, id_proveedor: int, fecha_registro: datetime):
        
        if precio_compra < 0 or precio_venta < 0:
            raise ValueError("Los precios no pueden ser negativos.")
        if existencia < 0:
            raise ValueError("La existencia no puede ser negativa.")

        self.id = id
        self.nombre = nombre
        self.id_categoria = id_categoria
        self.id_marca = id_marca
        self.descripcion = descripcion
        
        self._precio_compra = float(precio_compra)
        self._precio_venta = float(precio_venta)
        self._existencia = int(existencia)
        
        self.id_proveedor = id_proveedor          # ID del proveedor
        self.fecha_registro = fecha_registro
        
    def descontar_existencia(self, cantidad: int) -> None:
        """
        Registra una venta del producto, actualizando la existencia.
        
        Args:
            cantidad (int): Cantidad vendida.
        
        Raises:
            ValueError: Si la cantidad vendida es menor o igual a cero o si no hay suficiente existencia.
        """
        if cantidad <= 0:
            raise ValueError("La cantidad vendida debe ser mayor a cero.")
        if cantidad > self._existencia:
            raise ValueError("No hay suficiente existencia para realizar la venta.")
        
        self._existencia -= cantidad
        
