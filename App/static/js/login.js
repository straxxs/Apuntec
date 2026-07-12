/* ============ Toggle de visibilidad de contraseña ============ */
function togglePass(inputId, btn) {
    const input = document.getElementById(inputId);
    if (!input) return;
    const isPassword = input.type === "password";
    input.type = isPassword ? "text" : "password";
    btn.innerHTML = isPassword
        ? '<svg class="icon-eye" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/></svg>'
        : '<svg class="icon-eye" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>';
}

/* ============ Login ============ */
const loginForm = document.getElementById("loginForm");
if (loginForm) {
    loginForm.addEventListener("submit", function (e) {
        e.preventDefault();
        const btn = loginForm.querySelector('button[type="submit"]');
        const textoOriginal = btn.textContent;
        btn.disabled = true;
        btn.textContent = "Ingresando...";

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
            .catch(() => mostrarToast("Error de conexión. Intentá de nuevo.", "error"))
            .finally(() => {
                btn.disabled = false;
                btn.textContent = textoOriginal;
            });
    });
}
