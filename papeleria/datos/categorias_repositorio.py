from db import DatabaseManager

class CategoriaRepositorio:
    def __init__(self, db_config):
        self.db_config = db_config
        
    def obtener_categorias(self):
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute("SELECT * FROM categorias")
            return cursor.fetchall()
    
    def obtener_categoria(self, id: int):
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute("SELECT * FROM categoria WHERE id = %s", id)
            return cursor.fetchone()
    