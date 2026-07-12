"""
Política de validación de contraseñas y datos de usuario.
Basada en NIST SP 800-63B (estándar de seguridad de autenticación).
"""
import re

# ---------- Contraseñas ----------

# Contraseñas comunes prohibidas (lista reducida, las más usadas)
_CONTRASEÑAS_COMUNES = {
    "12345678", "password", "contraseña", "qwerty12", "abcdefg",
    "11111111", "00000000", "12341234", "admin123", "letmein1",
    "welcome1", "monkey12", "dragon12", "master12", "login123",
    "abc12345", "password1", "contrasena", "123456789", "1234567890",
}

_MINIMA_LONGITUD = 8
_MAXIMA_LONGITUD = 128


def validar_contraseña(contraseña):
    """
    Valida una contraseña contra la política NIST SP 800-63B.
    Devuelve (es_valida, lista_de_errores).
    """
    errores = []

    if not contraseña:
        return False, ["La contraseña es obligatoria."]

    if len(contraseña) < _MINIMA_LONGITUD:
        errores.append(f"Mínimo {_MINIMA_LONGITUD} caracteres.")

    if len(contraseña) > _MAXIMA_LONGITUD:
        errores.append(f"Máximo {_MAXIMA_LONGITUD} caracteres.")

    if not re.search(r"[A-Z]", contraseña):
        errores.append("Al menos 1 letra mayúscula.")

    if not re.search(r"[a-z]", contraseña):
        errores.append("Al menos 1 letra minúscula.")

    if not re.search(r"\d", contraseña):
        errores.append("Al menos 1 número.")

    if contraseña.lower().strip() in _CONTRASEÑAS_COMUNES:
        errores.append("Contraseña demasiado común. Elegí una más segura.")

    return len(errores) == 0, errores


def fortaleza_contraseña(contraseña):
    """
    Calcula la fortaleza de la contraseña (0-4).
    0: vacía, 1: débil, 2: regular, 3: buena, 4: excelente.
    """
    if not contraseña:
        return 0

    puntos = 0
    if len(contraseña) >= _MINIMA_LONGITUD:
        puntos += 1
    if len(contraseña) >= 12:
        puntos += 1
    if re.search(r"[A-Z]") and re.search(r"[a-z]"):
        puntos += 1
    if re.search(r"\d"):
        puntos += 1
    if re.search(r"[^A-Za-z0-9]"):
        puntos += 1

    return min(puntos, 4)


def mensaje_fortaleza(nivel):
    """Devuelve una etiqueta descriptiva para cada nivel de fortaleza."""
    etiquetas = {
        0: "",
        1: "Débil",
        2: "Regular",
        3: "Buena",
        4: "Excelente",
    }
    return etiquetas.get(nivel, "")


# ---------- Usuarios ----------

NOMBRE_PATTERN = re.compile(r"^[a-zA-Z0-9_]{3,20}$")


def validar_nombre_usuario(nombre):
    """
    Valida el nombre de usuario.
    - 3-20 caracteres
    - Solo letras, números y guión bajo
    - No puede empezar o terminar con guión bajo
    Devuelve (es_valido, lista_de_errores).
    """
    errores = []

    if not nombre:
        return False, ["El nombre de usuario es obligatorio."]

    if len(nombre) < 3:
        errores.append("Mínimo 3 caracteres.")
    if len(nombre) > 20:
        errores.append("Máximo 20 caracteres.")

    if not re.match(r"^[a-zA-Z0-9_]+$", nombre):
        errores.append("Solo letras, números y guión bajo (_).")

    if nombre.startswith("_") or nombre.endswith("_"):
        errores.append("No puede empezar ni terminar con _.")

    return len(errores) == 0, errores


def validar_email(email):
    """
    Validación de email más robusta que solo type="email".
    Devuelve (es_valido, lista_de_errores).
    """
    errores = []

    if not email:
        return False, ["El email es obligatorio."]

    email = email.strip()

    if len(email) > 254:
        errores.append("Email demasiado largo.")

    patron = re.compile(r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$")
    if not patron.match(email):
        errores.append("Formato de email inválido.")

    return len(errores) == 0, errores
