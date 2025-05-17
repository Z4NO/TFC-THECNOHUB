function cargarPostBloqueMedio(ruta, email = null, roomId = null) {
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





