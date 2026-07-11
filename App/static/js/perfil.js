const avatarActual = document.body.dataset.avatarActual;
const grid = document.getElementById("avatarGrid");
const inputElegido = document.getElementById("avatarElegido");
const preview = document.getElementById("avatarPreview");

if (grid && inputElegido && preview) {
    document.querySelectorAll(".avatar-opcion").forEach(img => {
        if (img.dataset.avatar === avatarActual) {
            img.classList.add("avatar-seleccionado");
        }

        img.addEventListener("click", function () {
            document.querySelectorAll(".avatar-opcion")
                .forEach(el => el.classList.remove("avatar-seleccionado"));
            this.classList.add("avatar-seleccionado");
            inputElegido.value = this.dataset.avatar;
            preview.src = this.src;
        });
    });
}

const formPerfil = document.getElementById("formPerfil");
if (formPerfil) formPerfil.addEventListener("submit", function (e) {
    e.preventDefault();
    fetch("/perfil/actualizar", { method: "POST", body: new FormData(this) })
        .then(res => res.json())
        .then(data => {
            mostrarToast(data.mensaje, data.ok ? "ok" : "error");
            if (data.ok) setTimeout(() => location.reload(), 800);
        })
        .catch(() => mostrarToast("Error de conexión", "error"));
});
