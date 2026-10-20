import os

import mysql.connector
from mysql.connector import Error
from mysql.connector.constants import ClientFlag
from dotenv import load_dotenv

# Lee las variables de un archivo .env (si existe). Si no existe, se usan
# los valores por defecto de abajo, que son los de nuestro XAMPP.
load_dotenv()


class DatabaseConfig:
    HOST = os.getenv('DB_HOST', 'localhost')
    PORT = int(os.getenv('DB_PORT', '3307'))      # nuestro MySQL corre en el 3307
    USER = os.getenv('DB_USER', 'root')
    PASSWORD = os.getenv('DB_PASSWORD', '')
    DATABASE = os.getenv('DB_NAME', 'flask_db_unilibre')

    @staticmethod
    def get_connection():
        """Abre una conexión nueva a MySQL. Devuelve None si no se pudo."""
        try:
            connection = mysql.connector.connect(
                host=DatabaseConfig.HOST,
                port=DatabaseConfig.PORT,
                user=DatabaseConfig.USER,
                password=DatabaseConfig.PASSWORD,
                database=DatabaseConfig.DATABASE,
                # rowcount cuenta las filas ENCONTRADAS (no solo las modificadas);
                # sin esto, un UPDATE con los mismos valores parecería "no encontrado"
                client_flags=[ClientFlag.FOUND_ROWS]
            )
            if connection.is_connected():
                return connection
        except Error as e:
            print(f"Error al conectar a MySQL: {e}")
        return None
