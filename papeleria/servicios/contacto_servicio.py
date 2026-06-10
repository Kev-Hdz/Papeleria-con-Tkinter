from dtos import ClienteDTO, ProveedorDTO
from datos import ContactoRepositorio

class ContactoServicio:
    def __init__(self, contacto_repositorio: ContactoRepositorio):
        self.repositorio = contacto_repositorio

    def registrar_cliente(self, datos: ClienteDTO) -> None:
        """Agrega un nuevo cliente a la base de datos.
        Args:
            datos (ClienteDTO): Una instancia de ClienteDTO con los datos del cliente a agregar.
        """
        self.repositorio.registrar_cliente(datos)

    def registrar_proveedor(self, datos: ProveedorDTO) -> None:
        """Agrega un nuevo proveedor a la base de datos.
        Args:
            datos (ProveedorDTO): Una instancia de ProveedorDTO con los datos del proveedor a agregar.
        """
        self.repositorio.registrar_proveedor(datos)

    def consultar_clientes(self):
        """Obtiene una lista de todos los clientes registrados en la base de datos.
        Returns:
            list: Una lista de instancias de Cliente. O una lista vacía si no hay clientes registrados.
        """
        return self.repositorio.consultar_clientes()
    
    def consultar_proveedores(self):
        """Obtiene una lista de todos los proveedores registrados en la base de datos.
        Returns:
            list: Una lista de instancias de Proveedor. O una lista vacía si no hay proveedores registrados.
        """
        return  self.repositorio.consultar_proveedores()
    
    def consultar_proveedor_por_id(self, id_proveedor: int) -> ProveedorDTO | None:
        """Consulta un proveedor por su ID.
        Args:
            id_proveedor (int): El ID del proveedor a consultar.
        Returns:
            Proveedor o None: El proveedor encontrado o None si no se encuentra ninguno.
        """
        return self.repositorio.consultar_proveedor_por_id(id_proveedor)

    def consultar_cliente_por_id(self, id_cliente: int) -> ClienteDTO | None:
        """Consulta un cliente por su ID.
        Args:
            id_cliente (int): El ID del cliente a consultar.
        Returns:
            Cliente o None: El cliente encontrado o None si no se encuentra ninguno.
        """
        return self.repositorio.consultar_cliente_por_id(id_cliente)
    
    def actualizar_proveedor(self, id_proveedor: int, datos: ProveedorDTO) -> None:
       existente = self.repositorio.consultar_proveedor_por_id(id_proveedor)
       if not existente:
        raise ValueError(f"No se encontró ningún proveedor con ID {id_proveedor}.")
       if not datos.nombre.strip():
        raise ValueError("El nombre del proveedor no puede estar vacío.")
       self.repositorio.actualizar_proveedor(id_proveedor, datos)
    
    def eliminar_proveedor(self, id_proveedor: int) -> None:
      existente = self.repositorio.consultar_proveedor_por_id(id_proveedor)
      if not existente:
        raise ValueError(f"No se encontró ningún proveedor con ID {id_proveedor}.")
      self.repositorio.eliminar_proveedor(id_proveedor)
    
    def actualizar_cliente(self, id_cliente: int, datos: ClienteDTO) -> None:
      existente = self.repositorio.consultar_cliente_por_id(id_cliente)
      if not existente:
        raise ValueError(f"No se encontró ningún cliente con ID {id_cliente}.")
      if not datos.nombre.strip():
        raise ValueError("El nombre del cliente no puede estar vacío.")
      self.repositorio.actualizar_cliente(id_cliente, datos)

    def eliminar_cliente(self, id_cliente: int) -> None:
      existente = self.repositorio.consultar_cliente_por_id(id_cliente)
      if not existente:
        raise ValueError(f"No se encontró ningún cliente con ID {id_cliente}.")
      self.repositorio.eliminar_cliente(id_cliente)
    



    