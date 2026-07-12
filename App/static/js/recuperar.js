const recuperarForm = document.getElementById("recuperarForm");
if (recuperarForm) recuperarForm.addEventListener("submit", function (e) {
    e.preventDefault();
    const btn = recuperarForm.querySelector('button[type="submit"]');
    const textoOriginal = btn.textContent;
    btn.disabled = true;
    btn.textContent = "Enviando...";

    fetch("/recuperar", { method: "POST", body: new FormData(this) })
        .then(res => res.json())
        .then(data => {
            mostrarToast(data.mensaje, data.ok ? "ok" : "error");
            if (data.enlace) {
                var div = document.getElementById("enlace-recuperacion") || document.createElement("div");
                div.id = "enlace-recuperacion";
                div.style.marginTop = "15px";
                div.style.padding = "14px";
                div.style.background = "var(--verde-light)";
                div.style.borderRadius = "8px";
                div.style.border = "1px solid var(--verde)";
                var p = document.createElement("p");
                p.style.margin = "0 0 8px";
                p.style.fontWeight = "600";
                p.style.color = "var(--verde-dark)";
                p.style.fontSize = "13px";
                p.textContent = "Enlace de recuperación:";
                var a = document.createElement("a");
                a.href = data.enlace;
                a.textContent = data.enlace;
                a.style.wordBreak = "break-all";
                a.style.color = "var(--celeste)";
                a.style.fontSize = "13px";
                a.style.fontWeight = "600";
                div.appendChild(p);
                div.appendChild(a);
                var form = document.getElementById("recuperarForm");
                form.parentNode.insertBefore(div, form.nextSibling);
            }
        })
        .catch(() => mostrarToast("Error de conexión. Intentá de nuevo.", "error"))
        .finally(() => {
            btn.disabled = false;
            btn.textContent = textoOriginal;
        });
});
