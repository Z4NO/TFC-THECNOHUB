document.addEventListener("DOMContentLoaded", function () {
    const botones = document.querySelectorAll(".button-container .button");
    const contenedorOpciones = document.querySelector(".contenedor-opcion-perfil");

    botones.forEach(button => {
        button.addEventListener("click", function () {
            const action = this.getAttribute("data-action");
            cargarComponente(action);
        });
    });
});

function cargarComponente(action) {
    let contenedor;
    let url = '';

    // Determinar en qué contenedor cargar el contenido
    if (action === 'foto' || action === 'nombre') {
        contenedor = document.querySelector('.contenedor-opcion-perfil');
    } else {
        contenedor = document.querySelector('.contenedor-opcion');
    }

    // Define la URL según la acción
    switch (action) {
        case 'perfil':
            url = '/static/profile_components/opciones-perfil.html';
            break;
        case 'foto':
            url = '/static/profile_components/actualizar_foto.html';
            break;
        case 'nombre':
            url = '/static/profile_components/editar-nombre.html';
            break;
        case 'actividad':
            url = '/static/profile_components/opciones-actividad.html';
            break;
        case 'Ajustes':
            url = '/static/profile_components/opciones-ajustes.html';
            break;
        default:
            contenedor.innerHTML = `<p>Selecciona una opción para ver su contenido.</p>`;
            return;
    }

    // Realiza la petición y carga el contenido dinámico
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('No se pudo cargar el componente');
            }
            return response.text();
        })
        .then(html => {
            contenedor.innerHTML = html;
        })
        .catch(error => {
            console.error('Error al cargar el componente:', error);
            contenedor.innerHTML = `<p>Error al cargar el contenido.</p>`;
        });
}


// Carga inicial al abrir la página
window.addEventListener('load', function () {
  cargarComponente('perfil'); 
});
