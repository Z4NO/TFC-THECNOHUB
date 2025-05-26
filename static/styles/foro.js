function cargarComponente(ruta) {
  fetch(ruta)
    .then(response => {
      if (!response.ok) {
        throw new Error(`Error al cargar el componente: ${response.statusText}`);
      }
      return response.text();
    })
    .then(html => {
      const medio = document.getElementById("bloqueMedio");
      const derecha = document.getElementById("bloqueDerecha");
      const izquierda = document.getElementById("bloqueIzquierda");

      // Cargar contenido en el bloque medio
      medio.innerHTML = html;

      // Ocultar los bloques laterales
      derecha.style.display = "none";

      // Expandir el bloque medio al 100%
      medio.style.width = "100vw"; 
      medio.style.maxWidth = "100%"; 
      medio.style.flexGrow = "1";
    })
    .catch(error => console.error("Error al cargar el componente:", error));
}

document.querySelectorAll('.posts').forEach(div => {
        div.addEventListener("click", function(e) {
            if (!e.target.closest('button')) {
                const commentBtn = div.querySelector('#boton-comentario');
                if (commentBtn) {
                    cargarPostForosNuevo(commentBtn, '/foro/main');
                }
            }
        });
    });


    function cargarPostForosNuevo(btn,ruta) {
        const foroid = btn.getAttribute("data-foro-id");
        const forodescripcion = btn.getAttribute("data-foro-descripcion");
        const forodueño = btn.getAttribute("data-foro-dueño");
        const forotitulo = btn.getAttribute("data-foro-titulo");
        fetch(`${ruta}?forodescripcion=${encodeURIComponent(forodescripcion)}&forodueño=${encodeURIComponent(forodueño)}&forotitulo=${encodeURIComponent(forotitulo)}&foroid=${foroid}`)
            .then(r => r.text())
            .then(html => {
            const medio = document.getElementById('foros');
            medio.innerHTML = html;
            setTimeout(() => {
                medio.style.height = '100%';
                medio.style.overflowY = 'auto';
            }, 100);
    
            
            })
            .catch(console.error);
    }
    function funcionLike(btn) {
        const numLikes = btn.nextElementSibling;
        if(btn.style.color == "red"){
            btn.style.color = "white"
            numLikes.innerHTML = parseInt(numLikes.innerHTML) - 1
        }else{
            btn.style.color = "red"
            numLikes.innerHTML = parseInt(numLikes.innerHTML) + 1
        }

    }