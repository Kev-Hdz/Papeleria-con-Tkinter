import mysql.connector
from mysql.connector import Error

# Clase para manejar la conexion a la base de datos usando el patron context manager (with)
class DatabaseManager:
    def __init__(self, config):
        self.config = config
        self.connection = None
        self.cursor = None

    def __enter__(self):
        """Inicializa la conexion y devuelve la instancia completa."""

        self.connection = mysql.connector.connect(**self.config)
        self.cursor = self.connection.cursor(dictionary=True)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Asegurar el cierre de la conexion al salir del bloque with."""

        if self.cursor:
            self.cursor.close()

        if self.connection:
            if exc_type is not None:
                self.connection.rollback()  # Revertir cambios en caso de error
                print(f"Transaccin revertida debido a: {exc_val}")
            else:
                self.connection.commit()  # Confirmar cambios si no hubo errores

            self.connection.close()

        return False  # No suprimir excepciones, si las hay
