document.addEventListener('DOMContentLoaded', function () {
    const contenedorOpcion = document.querySelector('.contenedor-opcion');
    const buttons = document.querySelectorAll('.button-container .button');
  
  
    buttons.forEach(button => {
      button.addEventListener('click', function () {
        const action = this.getAttribute('data-action');
        cargarComponente(action);
      });
    });
  
    function cargarComponente(action) {
      let url = '';
      switch (action) {
        case 'perfil':
          url = '/static/components/opciones-perfil.html';
          break;
        case 'actividad':
          url = '/static/components/opciones-actividad.html';
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
});

window.addEventListener('load', function () {
    cargarComponente('perfil'); 
});