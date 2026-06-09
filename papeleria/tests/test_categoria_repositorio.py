import pytest
from config import obtener_config_db
from datos.cliente_repositorio import ClienteRepositorio
from db import DatabaseManager
from modelos import Categoria
from datos import CategoriaRepositorio


# --- FIXTURE: PREPARACIÓN DEL ENTORNO ---
@pytest.fixture
def bd_limpia():
    """
    Fixture que limpia la tabla 'categorias' antes de ejecutar cada prueba 
    y reinicia el contador de IDs.
    """
    config = obtener_config_db()
    
    # Setup: Limpiar antes de la prueba
    with DatabaseManager(config) as cursor:
        # Desactivamos temporalmente las llaves foráneas por si hay tablas relacionadas
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        cursor.execute("TRUNCATE TABLE categorias;") # TRUNCATE borra todo y reinicia el AUTO_INCREMENT a 1
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
    
    # Ceder el control a la prueba pasando la configuración
    yield config
    
    # Teardown: (Opcional) Limpiar después de la prueba
    with DatabaseManager(config) as cursor:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        cursor.execute("TRUNCATE TABLE categorias;")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

# --- PRUEBAS ---

def test_agregar_y_obtener_por_id(bd_limpia):
    # 1. Arrange (Preparar)
    repo = CategoriaRepositorio(bd_limpia)
    categoria_1 = Categoria(nombre="Papelería")
    categoria_2 = Categoria(nombre="Escritorio")
    
    # 2. Act (Actuar)
    repo.agregar(categoria_1)
    repo.agregar(categoria_2)
    
    # Como usamos TRUNCATE en el fixture, estamos seguros de que esta categoría tendrá el ID 1
    categoria_recuperada = repo.obtener_por_id(1)
    categoria_recuperada_2 = repo.obtener_por_id(2)
    
    # 3. Assert (Afirmar)
    assert categoria_recuperada is not None
    assert categoria_recuperada.id == 1
    assert categoria_recuperada.nombre == "Papelería"
    assert categoria_recuperada_2 is not None
    assert categoria_recuperada_2.id == 2
    assert categoria_recuperada_2.nombre == "Escritorio"
    
    print(f"Categoría recuperada: ID={categoria_recuperada.id}, Nombre={categoria_recuperada.nombre}")
    print(f"Categoría recuperada: ID={categoria_recuperada_2.id}, Nombre={categoria_recuperada_2.nombre}")

def test_obtener_todos(bd_limpia):
    # 1. Arrange
    repo = CategoriaRepositorio(bd_limpia)
    
    # Verificamos que inicialmente la tabla esté vacía
    categorias_iniciales = repo.obtener_todos()
    assert len(categorias_iniciales) == 0
    
    # Agregamos dos categorías (nota que teléfono y correo son opcionales en tu modelo)
    repo.agregar(Categoria(nombre="Papelería"))
    repo.agregar(Categoria(nombre="Escritorio"))
    
    # 2. Act
    categorias_finales = repo.obtener_todos()
    
    # 3. Assert
    assert len(categorias_finales) == 2
    assert categorias_finales[0].nombre == "Papelería"
    assert categorias_finales[1].nombre == "Escritorio"
    
    print("Categorías recuperadas:")
    for cat in categorias_finales:
        print(f"ID={cat.id}, Nombre={cat.nombre}")