function cargarComponente(action) {
  let contenedor;
  let url = '';

  // Todos los componentes van en contenedor-opcion, excepto 'foto'
  if (action === 'foto' || action === 'nombre') {
      contenedor = document.querySelector('.contenedor-opcion-perfil'); // Solo 'foto' se carga aquí
  } else {
      contenedor = document.querySelector('.contenedor-opcion'); // Todos los demás van aquí
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
          url = '/static/profile_components/opciones_perfil/editar_nombre.html';
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

  // Realiza la petición y carga el contenido
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

// Evento para los botones de perfil y opciones
document.addEventListener('DOMContentLoaded', function () {
  const buttons = document.querySelectorAll('.button-container .button');

  buttons.forEach(button => {
      button.addEventListener('click', function () {
          const action = this.getAttribute('data-action');
          cargarComponente(action);
      });
  });
});

// Carga inicial al abrir la página
window.addEventListener('load', function () {
  cargarComponente('foto'); 
});
