function cargarPostBloqueMedio(ruta) {
  fetch(ruta)
    .then(r => r.text())
    .then(html => {
      const medio = document.getElementById('bloqueMedio');
      medio.innerHTML = html;

      
    })
    .catch(console.error);
}





