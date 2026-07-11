const AVATAR_DEFAULT = "uploads/avatares/no_avatar.png";

function escapeHtml(str) {
    if (!str) return '';
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

function htmlAvatar(nombre, avatarRuta, claseExtra = "avatar-chico") {
    const ruta = avatarRuta || AVATAR_DEFAULT;
    return `<img src="/static/${escapeHtml(ruta)}" alt="${escapeHtml(nombre || 'avatar')}" class="${escapeHtml(claseExtra)}">`;
}
