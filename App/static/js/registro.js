document.getElementById("registroForm").addEventListener("submit", function (e) {
    e.preventDefault();
    fetch("/registro", { method: "POST", body: new FormData(this) })
        .then(res => res.json())
        .then(data => {
            mostrarToast(data.mensaje, data.ok ? "ok" : "error");
            if (data.ok) setTimeout(() => window.location.href = "/login", 900);
        })
        .catch(() => mostrarToast("Hubo un error de conexión.", "error"));
});