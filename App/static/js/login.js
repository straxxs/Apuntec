const loginForm = document.getElementById("loginForm");
if (loginForm) loginForm.addEventListener("submit", function (e) {
    e.preventDefault();
    fetch("/login", { method: "POST", body: new FormData(this) })
        .then(res => res.json())
        .then(data => {
            mostrarToast(data.mensaje, data.ok ? "ok" : "error");
            if (data.ok) {
                setTimeout(() => {
                    if (data.rol === "admin") {
                        window.location.href = "/admin";
                    } else {
                        window.location.href = "/home";
                    }
                }, 700);
            }
        })
        .catch(() => mostrarToast("Hubo un error de conexión.", "error"));
});
