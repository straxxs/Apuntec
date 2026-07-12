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

/* ============ Validación de fortaleza en tiempo real ============ */
(function () {
    const passInput = document.getElementById("contraseña");
    const confirmInput = document.getElementById("confirmar_contraseña");
    const barra = document.getElementById("barra-fortaleza");
    const texto = document.getElementById("texto-fortaleza");
    const requisitos = document.getElementById("requisitos");
    const msgConfirmar = document.getElementById("msg-confirmar");
    const regForm = document.getElementById("registroForm");

    if (!passInput || !barra) return;

    function evaluarFortaleza(pass) {
        let nivel = 0;
        if (pass.length >= 8) nivel++;
        if (pass.length >= 12) nivel++;
        if (/[A-Z]/.test(pass) && /[a-z]/.test(pass)) nivel++;
        if (/\d/.test(pass)) nivel++;
        return Math.min(nivel, 4);
    }

    const etiquetas = { 0: "", 1: "Débil", 2: "Regular", 3: "Buena", 4: "Excelente" };
    const colores = { 0: "", 1: "var(--rojo)", 2: "var(--amarillo)", 3: "var(--celeste)", 4: "var(--verde)" };

    function actualizarRequisitos(pass) {
        if (!requisitos) return;
        const checks = {
            len: pass.length >= 8,
            mayus: /[A-Z]/.test(pass),
            minus: /[a-z]/.test(pass),
            num: /\d/.test(pass),
        };
        requisitos.querySelectorAll("li").forEach(li => {
            const req = li.getAttribute("data-req");
            if (req && checks[req] !== undefined) {
                li.classList.toggle("cumple", checks[req]);
            }
        });
    }

    function evaluarConfirmacion() {
        if (!confirmInput || !msgConfirmar) return;
        const pass = passInput.value;
        const confirm = confirmInput.value;
        if (!confirm) {
            msgConfirmar.textContent = "";
            msgConfirmar.style.color = "";
            return;
        }
        if (pass === confirm) {
            msgConfirmar.textContent = "Las contraseñas coinciden";
            msgConfirmar.style.color = "var(--verde-dark)";
        } else {
            msgConfirmar.textContent = "Las contraseñas no coinciden";
            msgConfirmar.style.color = "var(--rojo)";
        }
    }

    passInput.addEventListener("input", function () {
        const pass = this.value;
        const nivel = evaluarFortaleza(pass);

        // Barra
        barra.className = "barra-fortaleza" + (nivel > 0 ? " nivel-" + nivel : "");
        barra.style.setProperty("--fill-color", colores[nivel]);

        // Texto
        texto.textContent = etiquetas[nivel];
        texto.style.color = colores[nivel];

        // Requisitos
        actualizarRequisitos(pass);

        // Confirmación
        evaluarConfirmacion();
    });

    if (confirmInput) {
        confirmInput.addEventListener("input", evaluarConfirmacion);
    }

    /* ============ Envío del formulario ============ */
    if (regForm) {
        regForm.addEventListener("submit", function (e) {
            e.preventDefault();

            const btn = regForm.querySelector('button[type="submit"]');
            const textoOriginal = btn.textContent;
            btn.disabled = true;
            btn.textContent = "Creando cuenta...";

            fetch("/registro", { method: "POST", body: new FormData(regForm) })
                .then(res => res.json())
                .then(data => {
                    mostrarToast(data.mensaje, data.ok ? "ok" : "error");
                    if (data.ok) setTimeout(() => window.location.href = "/login", 900);
                })
                .catch(() => mostrarToast("Error de conexión. Intentá de nuevo.", "error"))
                .finally(() => {
                    btn.disabled = false;
                    btn.textContent = textoOriginal;
                });
        });
    }
})();
