from flask import Flask, render_template, request, redirect, url_for, session
from modulos.auth import login, registrar_usuario

app = Flask(__name__)
app.secret_key = "mitin_2026"

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form["nombre"]
        contraseña = request.form["contraseña"]

        if registrar_usuario(nombre, contraseña):
            return redirect(url_for("login_route"))
        else:
            return "Error al registrar"

    return render_template("registro.html")

@app.route("/login", methods=["GET", "POST"])
def login_route():
    if request.method == "POST":
        nombre = request.form["nombre"]
        contraseña = request.form["contraseña"]

        usuario = login(nombre, contraseña)

        if usuario:
            session["id_usuario"] = usuario["id"]
            session["nombre"] = usuario["nombre"]
            session["rol"] = usuario["rol"]

            return redirect(url_for("perfil"))
        else:
            return "Credenciales incorrectas"

    return render_template("login.html")


@app.route("/perfil")
def perfil():
    if "id_usuario" not in session:
        return redirect(url_for("login_route"))

    return f"Bienvenido {session['nombre']}"

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login_route"))





if __name__ == "__main__":
    app.run(debug=True)