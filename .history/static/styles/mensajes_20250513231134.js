function cargarComponente(ruta) {
  fetch(ruta)
    .then(res => res.text())
    .then(html => {
      const bloqueMedio = document.getElementById("bloqueMedio");
      if (bloqueMedio) {
        bloqueMedio.innerHTML = html;
        const socket = io({
          path: '/socket.io'
        }).connect(window.location.origin + '/mensajes/main/mensahjes');

        socket.on('connect', () => {
          console.log('🔌 Conectado a Socket.IO /mensajes');
        });

        socket.on('respuesta', data => {
          // inyectar cada mensaje entrante en .chat-mensajes
          const cont = bloqueMedio.querySelector('.chat-mensajes');
          const div = document.createElement('div');
          div.className = 'mensaje-contenedor recibido';
          div.innerHTML = `
            <div class="mensaje-imgPerfil"><img src="" alt="Perfil"/></div>
            <div class="mensaje-burbuja">
              <p>${data.msg}</p>
              <span class="mensaje-fecha">${new Date().toLocaleTimeString()}</span>
            </div>`;
          cont.appendChild(div);
          // opcional: hacer scroll abajo
          cont.scrollTop = cont.scrollHeight;
        });

        // 3) Enviar mensaje al pulsar el botón
        const btn = bloqueMedio.querySelector('.chat-input button');
        const txt = bloqueMedio.querySelector('.chat-input textarea');
        btn.addEventListener('click', () => {
          const msg = txt.value.trim();
          if (!msg) return;
          socket.emit('mensaje', { msg });
          // renderiza en pantalla localmente
          const cont = bloqueMedio.querySelector('.chat-mensajes');
          const div = document.createElement('div');
          div.className = 'mensaje-contenedor enviado';
          div.innerHTML = `
            <div class="mensaje-burbuja">
              <p>${msg}</p>
              <span class="mensaje-fecha">${new Date().toLocaleTimeString()}</span>
            </div>
            <div class="mensaje-imgPerfil"><img src="" alt="Mi foto"/></div>`;
          cont.appendChild(div);
          cont.scrollTop = cont.scrollHeight;
          txt.value = '';
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
