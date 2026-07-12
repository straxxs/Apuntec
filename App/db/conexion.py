import os
import pymysql
from urllib.parse import urlparse

def obtener_conexion():
    try:
        db_url = os.environ.get("DATABASE_URL")
        if db_url:
            parsed = urlparse(db_url)
            conn = pymysql.connect(
                host=parsed.hostname,
                user=parsed.username,
                password=parsed.password,
                database=parsed.path.lstrip("/"),
                port=int(parsed.port or 3306),
                ssl={"ssl_disabled": False},
            )
        else:
            conn = pymysql.connect(
                host="localhost",
                user="root",
                password="",
                database="apuntes_db"
            )
        return conn
    except pymysql.MySQLError as e:
        print(f"error al conectar la base de datos: {e}")
        return None
