function cargarComponente(ruta) {
  fetch(ruta)
    .then(res => res.text())
    .then(html => {
      const bloqueMedio = document.getElementById("bloqueMedio");
      if (bloqueMedio) {
        bloqueMedio.innerHTML = html;
        const socket = io({
          path: '/socket.io'
        }).connect(window.location.origin + '/mensajes');

        socket.on('connect', () => {
          console.log('🔌 Conectado a Socket.IO /mensajes');
        });
      } else {
        console.error("No se encontró el elemento con id bloqueMedio");
      }

      const bloqueDerecha = document.getElementById("bloqueDerecha");
      if (bloqueDerecha) {
        bloqueDerecha.hidden = true;
        bloqueDerecha.style.width = "0px";
        bloqueMedio.style.width = "100%";
      } else {
        console.error("No se encontró el elemento con id bloqueDerecha");
      }
    })
    .catch(err => {
      console.error("Error al cargar el componente:", err);
    });
}
