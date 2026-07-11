import pymysql
from db.conexion import obtener_conexion


# ---------------- CALIFICACIÓN (estrellas) ----------------

def calificar_apunte(id_alumno, id_apunte, calificacion, comentario=None):
    """Crea o actualiza la calificación (1-5) de un alumno sobre un apunte."""
    if calificacion < 1 or calificacion > 5:
        return False
    conn = obtener_conexion()
    if not conn:
        return False
    cursor = conn.cursor()
    try:
        # UPSERT: si ya calificó, actualiza; si no, inserta
        cursor.execute("""
            INSERT INTO Calificacion(calificacion, comentario, id_alumno, id_apunte)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE calificacion = VALUES(calificacion),
                                    comentario = VALUES(comentario)
        """, (calificacion, comentario, id_alumno, id_apunte))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error al calificar: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()


def obtener_promedio(id_apunte):
    """Devuelve (promedio, cantidad) de calificaciones de un apunte."""
    conn = obtener_conexion()
    if not conn:
        return (0, 0)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT AVG(calificacion), COUNT(*) FROM Calificacion WHERE id_apunte = %s
        """, (id_apunte,))
        avg, cant = cursor.fetchone()
        return (round(float(avg), 1) if avg else 0, cant or 0)
    except Exception as e:
        print(f"Error al obtener promedio: {e}")
        return (0, 0)
    finally:
        cursor.close()
        conn.close()


def calificacion_de(id_alumno, id_apunte):
    """Devuelve la calificación que le puso ESE alumno (o 0)."""
    conn = obtener_conexion()
    if not conn:
        return 0
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT calificacion FROM Calificacion WHERE id_alumno = %s AND id_apunte = %s",
            (id_alumno, id_apunte),
        )
        fila = cursor.fetchone()
        return fila[0] if fila else 0
    except Exception as e:
        print(f"Error: {e}")
        return 0
    finally:
        cursor.close()
        conn.close()


# ---------------- GUARDADOS ----------------

def alternar_guardado(id_alumno, id_apunte):
    """Si está guardado lo quita, si no lo agrega. Devuelve 'guardado' o 'quitado'."""
    conn = obtener_conexion()
    if not conn:
        return None
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT 1 FROM Guardado WHERE id_alumno = %s AND id_apunte = %s",
            (id_alumno, id_apunte),
        )
        if cursor.fetchone():
            cursor.execute(
                "DELETE FROM Guardado WHERE id_alumno = %s AND id_apunte = %s",
                (id_alumno, id_apunte),
            )
            conn.commit()
            return "quitado"
        else:
            cursor.execute(
                "INSERT INTO Guardado(id_alumno, id_apunte) VALUES (%s, %s)",
                (id_alumno, id_apunte),
            )
            conn.commit()
            return "guardado"
    except Exception as e:
        print(f"Error al alternar guardado: {e}")
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()


def esta_guardado(id_alumno, id_apunte):
    conn = obtener_conexion()
    if not conn:
        return False
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT 1 FROM Guardado WHERE id_alumno = %s AND id_apunte = %s",
            (id_alumno, id_apunte),
        )
        return cursor.fetchone() is not None
    except Exception:
        return False
    finally:
        cursor.close()
        conn.close()


def listar_guardados(id_alumno):
    """Apuntes que el alumno guardó (con datos básicos)."""
    conn = obtener_conexion()
    if not conn:
        return []
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute("""
            SELECT a.id, a.titulo, a.descripcion, a.id_materia,
                m.nombre AS materia, u.nombre AS autor
            FROM Guardado g
            JOIN Apunte a ON g.id_apunte = a.id
            LEFT JOIN Materia m ON a.id_materia = m.id
            LEFT JOIN Usuario u ON a.id_usuario_creador = u.id
            WHERE g.id_alumno = %s
            ORDER BY a.fecha_subida DESC
        """, (id_alumno,))
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al listar guardados: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


# ---------------- ME GUSTA (likes) ----------------

def alternar_me_gusta(id_usuario, id_apunte):
    """Si ya le dio me gusta lo quita, si no lo agrega. Devuelve 'gustado' o 'quitado'."""
    conn = obtener_conexion()
    if not conn:
        return None
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT 1 FROM me_gusta WHERE id_usuario = %s AND id_apunte = %s",
            (id_usuario, id_apunte),
        )
        if cursor.fetchone():
            cursor.execute(
                "DELETE FROM me_gusta WHERE id_usuario = %s AND id_apunte = %s",
                (id_usuario, id_apunte),
            )
            conn.commit()
            return "quitado"
        else:
            cursor.execute(
                "INSERT INTO me_gusta(id_usuario, id_apunte) VALUES (%s, %s)",
                (id_usuario, id_apunte),
            )
            conn.commit()
            return "gustado"
    except Exception as e:
        print(f"Error al alternar me gusta: {e}")
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()


def contar_me_gusta(id_apunte):
    """Devuelve la cantidad de 'me gusta' de un apunte."""
    conn = obtener_conexion()
    if not conn:
        return 0
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM me_gusta WHERE id_apunte = %s", (id_apunte,))
        return cursor.fetchone()[0]
    except Exception as e:
        print(f"Error: {e}")
        return 0
    finally:
        cursor.close()
        conn.close()


def me_gusta_de(id_usuario, id_apunte):
    """Devuelve True si el usuario le dio me gusta al apunte."""
    conn = obtener_conexion()
    if not conn:
        return False
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT 1 FROM me_gusta WHERE id_usuario = %s AND id_apunte = %s",
            (id_usuario, id_apunte),
        )
        return cursor.fetchone() is not None
    except Exception:
        return False
    finally:
        cursor.close()
        conn.close()