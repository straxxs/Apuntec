import pymysql
from db.conexion import obtener_conexion


def estadisticas_generales():
    """Métricas generales del sistema para el admin."""
    conn = obtener_conexion()
    if not conn:
        return {}
    cursor = conn.cursor()
    try:
        stats = {}

        cursor.execute("SELECT COUNT(*) FROM usuario")
        stats["total_usuarios"] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM usuario WHERE estado = 'activo'")
        stats["usuarios_activos"] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM usuario WHERE estado = 'bloqueado'")
        stats["usuarios_bloqueados"] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM curso")
        stats["total_cursos"] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM materia")
        stats["total_materias"] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM apunte")
        stats["total_apuntes"] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM apunte WHERE estado = 'aprobado'")
        stats["apuntes_aprobados"] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM apunte WHERE estado = 'pendiente'")
        stats["apuntes_pendientes"] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM apunte WHERE estado = 'rechazado'")
        stats["apuntes_rechazados"] = cursor.fetchone()[0]

        return stats
    except Exception as e:
        print(f"Error al obtener estadísticas: {e}")
        return {}
    finally:
        cursor.close()
        conn.close()


def apuntes_mas_valorados(limite=10):
    """Top apuntes con mejor promedio de estrellas."""
    conn = obtener_conexion()
    if not conn:
        return []
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute("""
            SELECT a.id, a.titulo, u.nombre AS autor,
                   ROUND(AVG(cal.calificacion), 1) AS promedio,
                   COUNT(DISTINCT cal.id) AS cant_calificaciones
            FROM Apunte a
            LEFT JOIN Calificacion cal ON cal.id_apunte = a.id
            LEFT JOIN Usuario u ON a.id_usuario_creador = u.id
            WHERE a.estado = 'aprobado'
            GROUP BY a.id
            HAVING cant_calificaciones > 0
            ORDER BY promedio DESC, cant_calificaciones DESC
            LIMIT %s
        """, (limite,))
        return cursor.fetchall()
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


def materias_mas_consultadas(limite=10):
    """Materias con más apuntes (proxy de consultas)."""
    conn = obtener_conexion()
    if not conn:
        return []
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute("""
            SELECT m.nombre AS materia,
                   c.anio, c.division,
                   COUNT(a.id) AS cantidad_apuntes
            FROM Materia m
            LEFT JOIN Apunte a ON a.id_materia = m.id AND a.estado = 'aprobado'
            LEFT JOIN Curso c ON m.id_curso = c.id
            GROUP BY m.id
            ORDER BY cantidad_apuntes DESC
            LIMIT %s
        """, (limite,))
        return cursor.fetchall()
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


def ranking_colaboradores(limite=10):
    """Top usuarios que más apuntes subieron (aprobados)."""
    conn = obtener_conexion()
    if not conn:
        return []
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute("""
            SELECT u.nombre AS autor, u.avatar,
                   COUNT(a.id) AS apuntes_subidos,
                   ROUND(AVG(cal.calificacion), 1) AS promedio_recibido
            FROM Apunte a
            JOIN Usuario u ON a.id_usuario_creador = u.id
            LEFT JOIN Calificacion cal ON cal.id_apunte = a.id
            WHERE a.estado = 'aprobado'
            GROUP BY u.id
            ORDER BY apuntes_subidos DESC
            LIMIT %s
        """, (limite,))
        return cursor.fetchall()
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


def apuntes_por_estado():
    """Cantidad de apuntes por estado (para gráfico pie)."""
    conn = obtener_conexion()
    if not conn:
        return []
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute("""
            SELECT estado, COUNT(*) AS cantidad
            FROM Apunte
            GROUP BY estado
        """)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


def apuntes_por_fecha(dias=30):
    """Apuntes subidos por día (para gráfico de línea)."""
    conn = obtener_conexion()
    if not conn:
        return []
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute("""
            SELECT DATE(fecha_subida) AS fecha, COUNT(*) AS cantidad
            FROM Apunte
            WHERE fecha_subida >= DATE_SUB(CURDATE(), INTERVAL %s DAY)
            GROUP BY DATE(fecha_subida)
            ORDER BY fecha ASC
        """, (dias,))
        return cursor.fetchall()
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        cursor.close()
        conn.close()
