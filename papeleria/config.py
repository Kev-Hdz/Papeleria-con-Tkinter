import os
from dotenv import load_dotenv

def obtener_config_db():
    """Carga las variables del .env y devuelve el diccionario de conexión."""
    # Carga las variables de entorno desde el archivo .env
    load_dotenv()
    
    return {
        'host': os.environ.get('DB_HOST'),
        'user': os.environ.get('DB_USER'),
        'password': os.environ.get('DB_PASSWORD'),
        'database': os.environ.get('DB_NAME'),
        'port': int(os.environ.get('DB_PORT'), 3306)  # Puerto por defecto de MySQL
    }