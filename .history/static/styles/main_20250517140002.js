function cargarPostBloqueMedio()
{
    var bloqueMedio = document.getElementById("bloque-medio");
    var url = "https://jsonplaceholder.typicode.com/posts";
    fetch(url)
        .then(response => response.json())
        .then(data => {
            data.forEach(post => {
                var postDiv = document.createElement("div");
                postDiv.className = "post";
                postDiv.innerHTML = `
                    <h2>${post.title}</h2>
                    <p>${post.body}</p>
                `;
                bloqueMedio.appendChild(postDiv);
            });
        })
        .catch(error => console.error('Error:', error));
}