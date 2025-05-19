document.addEventListener("DOMContentLoaded", function() {
    const explorarBtn = document.querySelector(".funcionalidadesbtn:nth-child(2)"); 
    const funcionalidadBtns = document.querySelectorAll(".funcionalidadesbtn"); // Selecciona todos los botones
    const searchBar = document.getElementById("search-bar");
    const bloqueMedio = document.getElementById("bloqueMedio");
    const bloqueIzquierda = document.querySelector(".bloqueIzquierda");
    const bloqueDerecha = document.querySelector(".bloqueDerecha");
    const searchBtn = document.getElementById("search-btn");
    const searchInput = document.getElementById("search-input"); 
    const resultadoContainer = document.createElement("div");

    searchBar.appendChild(resultadoContainer);

    explorarBtn.addEventListener("click", function() {
        if (searchBar.style.display === "none") {
            searchBar.style.display = "flex";
            bloqueMedio.style.marginTop = "80px";
            bloqueIzquierda.style.marginTop = "80px";
            bloqueDerecha.style.marginTop = "80px";
        } else {
            searchBar.style.display = "none";
            bloqueMedio.style.marginTop = "0px";
            bloqueIzquierda.style.marginTop = "0px";
            bloqueDerecha.style.marginTop = "0px";
        }
    });

    funcionalidadBtns.forEach(btn => {
        if (btn !== explorarBtn) { 
            btn.addEventListener("click", function() {
                if (searchBar.style.display === "flex") {
                    searchBar.style.display = "none";
                    bloqueMedio.style.marginTop = "0px";
                    bloqueIzquierda.style.marginTop = "0px";
                    bloqueDerecha.style.marginTop = "0px";
                }
            });
        }
    });

    function realizarBusqueda() {
        let searchText = encodeURIComponent(searchInput.value);

        fetch(`/buscar?valor=${searchText}`)
            .then(response => response.json())
            .then(data => {
                resultadoContainer.innerHTML = "";

                
                fetch('/funciones', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ funcion: 'funcion1', parametros: searchInput.value })
                })
                .then(response => response.json())
                .then(result => {
                    resultadoContainer.innerHTML = "";
                    // Puedes mostrar el resultado devuelto por la función aquí
                    resultadoContainer.textContent = JSON.stringify(result);
                })
                .catch(error => {
                    resultadoContainer.innerHTML = "<p>Error al llamar a la función.</p>";
                    console.error("Error en la llamada a la función:", error);
                });
            })
            .catch(error => console.error("Error en la búsqueda:", error));
    }

  
    searchInput.addEventListener("keydown", function(event) {
        if (event.key === "Enter") { 
            event.preventDefault(); 
            realizarBusqueda();
        }
    });


    searchBtn.addEventListener("click", realizarBusqueda);
});
