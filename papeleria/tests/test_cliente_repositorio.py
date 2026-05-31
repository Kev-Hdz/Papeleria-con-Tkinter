import pytest
from config import obtener_config_db
from db import DatabaseManager
from modelos import Cliente
from datos import ClienteRepositorio

# --- FIXTURE: PREPARACIÓN DEL ENTORNO ---
@pytest.fixture
def bd_limpia():
    """
    Fixture que limpia la tabla 'clientes' antes de ejecutar cada prueba 
    y reinicia el contador de IDs.
    """
    config = obtener_config_db()
    
    # Setup: Limpiar antes de la prueba
    with DatabaseManager(config) as cursor:
        # Desactivamos temporalmente las llaves foráneas por si hay tablas relacionadas
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        cursor.execute("TRUNCATE TABLE clientes;") # TRUNCATE borra todo y reinicia el AUTO_INCREMENT a 1
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
    
    # Ceder el control a la prueba pasando la configuración
    yield config
    
    # Teardown: (Opcional) Limpiar después de la prueba
    with DatabaseManager(config) as cursor:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        cursor.execute("TRUNCATE TABLE clientes;")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

# --- PRUEBAS ---

def test_agregar_y_obtener_por_id(bd_limpia):
    # 1. Arrange (Preparar)
    repo = ClienteRepositorio(bd_limpia)
    nuevo_cliente = Cliente(nombre="Juan Perez", telefono="9931234567", correo="juan@mail.com")
    
    # 2. Act (Actuar)
    repo.agregar(nuevo_cliente)
    
    # Como usamos TRUNCATE en el fixture, estamos seguros de que este cliente tendrá el ID 1
    cliente_recuperado = repo.obtener_por_id(1)
    
    # 3. Assert (Afirmar)
    assert cliente_recuperado is not None
    assert cliente_recuperado.id == 1
    assert cliente_recuperado.nombre == "Juan Perez"
    assert cliente_recuperado.telefono == "9931234567"
    assert cliente_recuperado.correo == "juan@mail.com"

def test_obtener_todos(bd_limpia):
    # 1. Arrange
    repo = ClienteRepositorio(bd_limpia)
    
    # Verificamos que inicialmente la tabla esté vacía
    clientes_iniciales = repo.obtener_todos()
    assert len(clientes_iniciales) == 0
    
    # Agregamos dos clientes (nota que teléfono y correo son opcionales en tu modelo)
    repo.agregar(Cliente(nombre="Cliente Uno"))
    repo.agregar(Cliente(nombre="Cliente Dos"))
    
    # 2. Act
    clientes_finales = repo.obtener_todos()
    
    # 3. Assert
    assert len(clientes_finales) == 2
    assert clientes_finales[0].nombre == "Cliente Uno"
    assert clientes_finales[1].nombre == "Cliente Dos"