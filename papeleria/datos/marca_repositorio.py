from db import DatabaseManager

class MarcaRepositorio:
    def __init__(self, db_config):
        self.db_config = db_config
        
    def obtener_marcas(self):
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute("SELECT * FROM marcas")
            return cursor.fetchall()
    
    def obtener_marca(self, id: int):
        with DatabaseManager(self.db_config) as cursor:
            cursor.execute("SELECT * FROM marcas WHERE id = %s", id)
            return cursor.fetchone()
    