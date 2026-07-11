import pymysql
from db.conexion import obtener_conexion


def registrar_accion(id_usuario, accion, detalle=None, ip=None):
    """Registra una acción en el log de auditoría."""
    conn = obtener_conexion()
    if not conn:
        return False
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO audit_log (id_usuario, accion, detalle, ip, fecha)
            VALUES (%s, %s, %s, %s, NOW())
        """, (id_usuario, accion, detalle, ip))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error en auditoría: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()


def listar_auditoria(id_curso=None, limite=100):
    """Devuelve los últimos registros de auditoría."""
    conn = obtener_conexion()
    if not conn:
        return []
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        if id_curso:
            cursor.execute("""
                SELECT al.id, al.id_usuario, u.nombre AS usuario,
                       al.accion, al.detalle, al.ip, al.fecha
                FROM audit_log al
                LEFT JOIN Usuario u ON al.id_usuario = u.id
                LEFT JOIN Curso c ON u.id_curso = c.id
                WHERE c.id = %s OR al.id_usuario IS NULL
                ORDER BY al.fecha DESC
                LIMIT %s
            """, (id_curso, limite))
        else:
            cursor.execute("""
                SELECT al.id, al.id_usuario, u.nombre AS usuario,
                       al.accion, al.detalle, al.ip, al.fecha
                FROM audit_log al
                LEFT JOIN Usuario u ON al.id_usuario = u.id
                ORDER BY al.fecha DESC
                LIMIT %s
            """, (limite,))
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al listar auditoría: {e}")
        return []
    finally:
        cursor.close()
        conn.close()
