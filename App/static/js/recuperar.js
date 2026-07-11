const recuperarForm = document.getElementById("recuperarForm");
if (recuperarForm) recuperarForm.addEventListener("submit", function (e) {
    e.preventDefault();
    fetch("/recuperar", { method: "POST", body: new FormData(this) })
        .then(res => res.json())
        .then(data => {
            mostrarToast(data.mensaje, data.ok ? "ok" : "error");
            if (data.enlace) {
                var div = document.getElementById("enlace-recuperacion") || document.createElement("div");
                div.id = "enlace-recuperacion";
                div.style.marginTop = "15px";
                div.style.padding = "12px";
                div.style.background = "#e8f5e9";
                div.style.borderRadius = "8px";
                var a = document.createElement("a");
                a.href = data.enlace;
                a.textContent = data.enlace;
                a.style.wordBreak = "break-all";
                a.style.color = "#1565c0";
                var p = document.createElement("p");
                p.style.margin = "0 0 8px";
                p.style.fontWeight = "bold";
                p.style.color = "#2e7d32";
                p.textContent = "Enlace de recuperación:";
                div.appendChild(p);
                div.appendChild(a);
                var form = document.getElementById("recuperarForm");
                form.parentNode.insertBefore(div, form.nextSibling);
            }
        })
        .catch(() => mostrarToast("Hubo un error de conexión.", "error"));
});
