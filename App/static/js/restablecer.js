const form = document.getElementById("restablecerForm");
if (form) {
    form.addEventListener("submit", function (e) {
        e.preventDefault();
        const token = this.dataset.token;
        const contraseña = document.getElementById("contraseña").value;
        const confirmar = document.getElementById("confirmar").value;

        if (contraseña !== confirmar) {
            mostrarToast("Las contraseñas no coinciden.", "error");
            return;
        }
        if (contraseña.length < 4) {
            mostrarToast("La contraseña debe tener al menos 4 caracteres.", "error");
            return;
        }

        const fd = new FormData();
        fd.append("contraseña", contraseña);
        fetch("/restablecer/" + token, { method: "POST", body: fd })
            .then(res => res.json())
            .then(data => {
                mostrarToast(data.mensaje, data.ok ? "ok" : "error");
                if (data.ok) setTimeout(() => window.location.href = "/login", 1200);
            })
            .catch(() => mostrarToast("Hubo un error de conexión.", "error"));
    });
}
