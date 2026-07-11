import secrets
import datetime
import pymysql
from db.conexion import obtener_conexion


def generar_token(id_usuario):
    """Genera un token de recuperación y lo guarda en la BD."""
    token = secrets.token_urlsafe(32)
    expira = datetime.datetime.now() + datetime.timedelta(hours=2)
    conn = obtener_conexion()
    if not conn:
        return None
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO password_reset_tokens (id_usuario, token, expira_en) VALUES (%s, %s, %s)",
            (id_usuario, token, expira),
        )
        conn.commit()
        return token
    except Exception as e:
        print(f"Error al generar token: {e}")
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()


def validar_token(token):
    """Devuelve el id_usuario si el token es válido, o None."""
    conn = obtener_conexion()
    if not conn:
        return None
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute(
            "SELECT id_usuario FROM password_reset_tokens WHERE token = %s AND usado = 0 AND expira_en > NOW()",
            (token,),
        )
        fila = cursor.fetchone()
        return fila["id_usuario"] if fila else None
    except Exception as e:
        print(f"Error al validar token: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def marcar_token_usado(token):
    """Marca un token como usado."""
    conn = obtener_conexion()
    if not conn:
        return False
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE password_reset_tokens SET usado = 1 WHERE token = %s", (token,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error al marcar token: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()


def resetear_contraseña(token, nueva_contraseña):
    """Resetea la contraseña del usuario asociado al token."""
    from modulos.auth import hashear_contraseña

    id_usuario = validar_token(token)
    if not id_usuario:
        return False

    conn = obtener_conexion()
    if not conn:
        return False
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE usuario SET contrasena = %s WHERE id = %s",
            (hashear_contraseña(nueva_contraseña), id_usuario),
        )
        cursor.execute("UPDATE password_reset_tokens SET usado = 1 WHERE token = %s", (token,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error al resetear contraseña: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()


def obtener_usuario_por_email(email):
    """Busca un usuario por email."""
    conn = obtener_conexion()
    if not conn:
        return None
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute("SELECT id, nombre, email FROM usuario WHERE email = %s", (email,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Error al buscar usuario por email: {e}")
        return None
    finally:
        cursor.close()
        conn.close()
