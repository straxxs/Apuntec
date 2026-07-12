// Sistema de notificaciones tipo "toast"
// Uso: mostrarToast("Mensaje", "ok" | "error")

function mostrarToast(mensaje, tipo = "ok") {
    // Crear contenedor si no existe
    let cont = document.getElementById("toast-container");
    if (!cont) {
        cont = document.createElement("div");
        cont.id = "toast-container";
        document.body.appendChild(cont);
    }

    const toast = document.createElement("div");
    toast.className = "toast toast-" + tipo;
    toast.textContent = mensaje;
    cont.appendChild(toast);

    // Sonido
    if (typeof sonidoExito === "function" && tipo === "ok") sonidoExito();
    else if (typeof sonidoError === "function" && tipo === "error") sonidoError();

    // Animación de entrada
    requestAnimationFrame(() => toast.classList.add("toast-visible"));

    // Salir a los 3 segundos
    setTimeout(() => {
        toast.classList.remove("toast-visible");
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}