// cargarComponente.js
function cargarComponente(ruta) {
  fetch(ruta)
    .then(res => res.text())
    .then(html => {
      const medio = document.getElementById("bloqueMedio");
      medio.innerHTML = html;

      // 1) Arranco Socket.IO en el namespace correcto
      const socket = io('/main/mensajes', { path: '/socket.io' });

      socket.on('connect', () =>
        console.log('🔌 Conectado a /main/mensajes')
      );

      // 2) Recibo y renderizo respuestas
      socket.on('send_mensaje', data => {
        const cont = medio.querySelector('.chat-mensajes');
        const div = document.createElement('div');
        div.className = 'mensaje-contenedor recibido';
        div.innerHTML = `
          <div class="mensaje-imgPerfil">
            <img src="" alt="Perfil"/>
          </div>
          <div class="mensaje-burbuja">
            <p>${data.response}</p>
            <span class="mensaje-fecha">
              ${new Date().toLocaleTimeString()}
            </span>
          </div>`;
        cont.appendChild(div);
        cont.scrollTop = cont.scrollHeight;
      });

      // 3) Envío mensajes
      const btn = medio.querySelector('.chat-input button');
      const txt = medio.querySelector('.chat-input textarea');
      btn.addEventListener('click', () => {
        const msg = txt.value.trim();
        if (!msg) return;
        socket.emit('send_mensaje', { msg });
        // render local
        const cont = medio.querySelector('.chat-mensajes');
        const div = document.createElement('div');
        div.className = 'mensaje-contenedor enviado';
        div.innerHTML = `
          <div class="mensaje-burbuja">
            <p>${msg}</p>
            <span class="mensaje-fecha">
              ${new Date().toLocaleTimeString()}
            </span>
          </div>
          <div class="mensaje-imgPerfil">
            <img src="" alt="Mi foto"/>
          </div>`;
        cont.appendChild(div);
        cont.scrollTop = cont.scrollHeight;
        txt.value = '';
      });

      // 4) Ocultar la columna derecha
      const derecha = document.getElementById("bloqueDerecha");
      derecha.hidden = true;
      derecha.style.width = "0";
      medio.style.width = "100%";
    })
    .catch(err => console.error("Error al cargar componente:", err));
}
