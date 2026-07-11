// ---------- Datos del curso (leídos del <body>) ----------
const ID_CURSO = document.body.dataset.idCurso;
const PUEDE_GESTIONAR = document.body.dataset.puedeGestionar === "true";


// ---------- Materias ----------
function cargarMaterias() {
        fetch(`/cursos/${ID_CURSO}/materias`)
        .then(res => res.json())
        .then(data => {
            const tabla = document.getElementById("tablaMaterias");
            tabla.innerHTML = "";

            if (!data.materias || data.materias.length === 0) {
                tabla.innerHTML = '<tr><td colspan="3" class="vacio">No hay materias todavía.</td></tr>';
                return;
            }

            data.materias.forEach(m => {
                const tr = document.createElement("tr");

                let acciones = `
                    <a href="/materia/${m.id}" class="btn btn-celeste btn-chico">Entrar</a>`;

                if (PUEDE_GESTIONAR) {
                    const nombreSeguro = (m.nombre || "").replace(/'/g, "\\'");
                    const profeSeguro = (m.nombre_profesor || "").replace(/'/g, "\\'");
                    acciones += `
                        <button class="btn btn-amarillo btn-chico"
                            onclick="editarMateria(${m.id}, '${nombreSeguro}', '${profeSeguro}')">
                            Editar
                        </button>
                        <button class="btn btn-rojo btn-chico" onclick="borrarMateria(${m.id})">
                            Eliminar
                        </button>`;
                }

                tr.innerHTML = `
                    <td>${escapeHtml(m.nombre)}</td>
                    <td>${escapeHtml(m.nombre_profesor || "-")}</td>
                    <td class="acciones">${acciones}</td>`;
                tabla.appendChild(tr);
            });
        });
}


// ---------- Alumnos ----------
function cargarAlumnos() {
    fetch(`/cursos/${ID_CURSO}/alumnos`)
        .then(res => res.json())
        .then(data => {
            const lista = document.getElementById("listaAlumnos");
            lista.innerHTML = "";

            if (!data.alumnos || data.alumnos.length === 0) {
                lista.innerHTML = '<li class="vacio">No hay integrantes.</li>';
                return;
            }

            data.alumnos.forEach(a => {
                const li = document.createElement("li");

                let boton = "";
                // Solo el que gestiona puede ascender, y solo a alumnos
                if (PUEDE_GESTIONAR && a.rol === "alumno") {
                    boton = `<button class="btn btn-celeste btn-chico"
                                onclick="hacerModerador(${a.id})">Hacer moderador</button>`;
                }

                li.innerHTML = `
                    <span class="autor-linea" style="margin-bottom:0;">
                        ${htmlAvatar(a.nombre, a.avatar, "avatar-chico")}
                        <span>${escapeHtml(a.nombre)}</span>
                    </span>
                    <span style="display:flex;align-items:center;gap:8px;">
                        <span class="badge-rol rol-${escapeHtml(a.rol)}">${escapeHtml(a.rol)}</span>
                        ${boton}
                    </span>`;
                lista.appendChild(li);
            });
        });
}


// ---------- Crear materia ----------
const formMateria = document.getElementById("formMateria");
if (formMateria) {
    formMateria.addEventListener("submit", function (e) {
        e.preventDefault();
        const fd = new FormData(this);
        fd.append("id_curso", ID_CURSO);
        fetch("/materias/crear", { method: "POST", body: fd })
            .then(res => res.json())
            .then(data => {
                mostrarToast(data.mensaje, data.ok ? "ok" : "error");
                if (data.ok) { this.reset(); cargarMaterias(); }
            })
            .catch(() => mostrarToast("Error de conexión", "error"));
    });
}


// ---------- Editar materia ----------
function editarMateria(id, nombreActual, profesorActual) {
    const nombre = prompt("Nuevo nombre de la materia:", nombreActual);
    if (nombre === null) return;
    const profesor = prompt("Nombre del profesor (vacío = sin profesor):", profesorActual);

    const fd = new FormData();
    fd.append("nombre", nombre);
    fd.append("profesor", profesor || "");

    fetch(`/materias/editar/${id}`, { method: "POST", body: fd })
        .then(res => res.json())
        .then(data => {
            mostrarToast(data.mensaje, data.ok ? "ok" : "error");
            if (data.ok) cargarMaterias();
        })
        .catch(() => mostrarToast("Error de conexión", "error"));
}


// ---------- Borrar materia ----------
function borrarMateria(id) {
    if (!confirm("¿Eliminar esta materia? Se perderán sus apuntes.")) return;
    fetch(`/materias/eliminar/${id}`, { method: "POST" })
        .then(res => res.json())
        .then(data => {
            mostrarToast(data.mensaje, data.ok ? "ok" : "error");
            if (data.ok) cargarMaterias();
        })
        .catch(() => mostrarToast("Error de conexión", "error"));
}


// ---------- Editar curso ----------
const formEditarCurso = document.getElementById("formEditarCurso");
if (formEditarCurso) {
    formEditarCurso.addEventListener("submit", function (e) {
        e.preventDefault();
        fetch(`/cursos/editar/${ID_CURSO}`, { method: "POST", body: new FormData(this) })
            .then(res => res.json())
            .then(data => {
                mostrarToast(data.mensaje, data.ok ? "ok" : "error");
                if (data.ok) setTimeout(() => location.reload(), 800);
            })
            .catch(() => mostrarToast("Error de conexión", "error"));
    });
}


// ---------- Copiar código de invitación ----------
function copiarCodigo(codigo) {
    navigator.clipboard.writeText(codigo)
        .then(() => mostrarToast("Código copiado: " + codigo, "ok"))
        .catch(() => mostrarToast("Código del curso: " + codigo, "ok"));
}

// ---------- Ascender alumno a moderador ----------
function hacerModerador(idUsuario) {
    if (!confirm("¿Convertir a este alumno en moderador del curso?")) return;
    const fd = new FormData();
    fd.append("id_usuario", idUsuario);
    fetch(`/cursos/${ID_CURSO}/ascender`, { method: "POST", body: fd })
        .then(res => res.json())
        .then(data => {
            mostrarToast(data.mensaje, data.ok ? "ok" : "error");
            if (data.ok) cargarAlumnos();
        })
        .catch(() => mostrarToast("Error de conexión", "error"));
}
// ---------- Apuntes pendientes (moderación) ----------
function cargarPendientes() {
    if (!PUEDE_GESTIONAR) return;
    fetch(`/cursos/${ID_CURSO}/pendientes`)
        .then(res => res.json())
        .then(data => {
            const cont = document.getElementById("listaPendientes");
            if (!cont) return;
            cont.innerHTML = "";

            if (!data.apuntes || data.apuntes.length === 0) {
                cont.innerHTML = '<p class="vacio">No hay apuntes pendientes. 🎉</p>';
                return;
            }

            data.apuntes.forEach(a => {
                const archivos = (a.archivos || []).map(f =>
                    `<a class="btn btn-celeste btn-chico" href="/static/${f.ruta}" target="_blank">Ver ${f.tipo}</a>`
                ).join(" ");
                const div = document.createElement("div");
                div.className = "card";
                div.style.marginBottom = "12px";
                div.innerHTML = `
                    <strong>${escapeHtml(a.titulo)}</strong> — <em>${escapeHtml(a.materia || "")}</em><br>
                    <span>Por ${escapeHtml(a.autor)}</span>
                    <p>${escapeHtml(a.descripcion || "")}</p>
                    <div class="acciones">
                        ${archivos}
                        <button class="btn btn-amarillo btn-chico" onclick="aprobar(${a.id})">✅ Aprobar</button>
                        <button class="btn btn-rojo btn-chico" onclick="rechazar(${a.id})">❌ Rechazar</button>
                    </div>`;
                cont.appendChild(div);
            });
        });
}

function aprobar(id) {
    fetch(`/apuntes/${id}/aprobar`, { method: "POST" })
        .then(res => res.json())
        .then(data => { mostrarToast(data.mensaje, data.ok ? "ok" : "error"); if (data.ok) cargarPendientes(); })
        .catch(() => mostrarToast("Error de conexión", "error"));
}

function rechazar(id) {
    fetch(`/apuntes/${id}/rechazar`, { method: "POST" })
        .then(res => res.json())
        .then(data => { mostrarToast(data.mensaje, data.ok ? "ok" : "error"); if (data.ok) cargarPendientes(); })
        .catch(() => mostrarToast("Error de conexión", "error"));
}

cargarMaterias();
cargarAlumnos();
cargarPendientes();