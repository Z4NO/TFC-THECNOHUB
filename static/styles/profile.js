function cargarComponente(action) {
  const contenedorOpcion = document.querySelector('.contenedor-opcion');
  let url = '';
  switch (action) {
    case 'perfil':
      url = '/static/profile_components/opciones-perfil.html';
      break;
    case 'actividad':
      url = '/static/profile_components/opciones-actividad.html';
      break;
    case 'Ajustes':
      url = '/static/profile_components/opciones-ajustes.html';
      break;
    default:
      contenedorOpcion.innerHTML = `<p>Selecciona una opción para ver su contenido.</p>`;
      return;
  }

  fetch(url)
    .then(response => {
      if (!response.ok) {
        throw new Error('No se pudo cargar el componente');
      }
      return response.text();
    })
    .then(html => {
      contenedorOpcion.innerHTML = html;
    })
    .catch(error => {
      console.error('Error al cargar el componente:', error);
      contenedorOpcion.innerHTML = `<p>Error al cargar el contenido.</p>`;
    });
}


document.addEventListener('DOMContentLoaded', function () {
    const buttons = document.querySelectorAll('.button-container .button');
  
  
    buttons.forEach(button => {
      button.addEventListener('click', function () {
        const action = this.getAttribute('data-action');
        cargarComponente(action);
      });
    });
  
});

window.addEventListener('load', function () {
    cargarComponente('perfil'); 
});