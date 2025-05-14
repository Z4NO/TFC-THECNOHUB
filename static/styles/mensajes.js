// Variable global
let socket = null;
let currentRoom = null;




// Inicializa Socket.IO y handler de mensajes entrantes
function initSocket() {
  if (!socket) {
    socket = io('/main/mensajes', { path: '/socket.io' });
    socket.on('connect', () =>
      console.log('🔌 Conectado a /main/mensajes')
    );
    socket.on('respuesta', ({ msg }) => {
      renderIncomingMessage(msg);
    });
  }
}

// Renderiza un mensaje recibido
function renderIncomingMessage(msg) {
  const cont = document.querySelector('#bloqueMedio .chat-mensajes');
  if (!cont) return;
  const div = document.createElement('div');
  div.className = 'mensaje-contenedor recibido';
  div.innerHTML = `
    <div class="mensaje-imgPerfil"><img src="" alt="Perfil"/></div>
    <div class="mensaje-burbuja">
      <p>${msg}</p>
      <span class="mensaje-fecha">${new Date().toLocaleTimeString()}</span>
    </div>`;
  cont.appendChild(div);
  cont.scrollTop = cont.scrollHeight;
}

// Renderiza un mensaje enviado localmente
function renderOutgoingMessage(msg) {
  const cont = document.querySelector('#bloqueMedio .chat-mensajes');
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
}

// Carga la UI y si hay room/email, engancha el envío
function cargarComponente(ruta, email = null, roomId = null) {
  fetch(ruta)
    .then(r => r.text())
    .then(html => {
      const medio = document.getElementById('bloqueMedio');
      medio.innerHTML = html;
      document.getElementById('bloqueDerecha').hidden = true;
      medio.style.width = '100%';

      medio.querySelectorAll('.mensajes').forEach(btn => {
      btn.addEventListener('click', () => {
        console.log('🔄 Cambiando de sala');
        const otherEmail = btn.dataset.email;
        const roomId     = btn.dataset.room;
        initSocket();

        // salir de la sala anterior
        if (currentRoom) {
          socket.emit('leave', { room: currentRoom });
        }
        // unirse a la nueva
        socket.emit('join',  { room: roomId, email: otherEmail });
        currentRoom = roomId;

        // cargar UI + habilitar envío
        cargarComponente('/mensajes/main/mensajes', otherEmail, roomId);
      });
      });

      if (roomId && email) {
        const btn = medio.querySelector('.chat-input button');
        const txt = medio.querySelector('.chat-input textarea');
        btn.onclick = () => {
          const msg = txt.value.trim();
          if (!msg) return;
          socket.emit('send_mensaje', { room: roomId, msg });
          renderOutgoingMessage(msg);
          txt.value = '';
        };
      }
    })
    .catch(console.error);
}





