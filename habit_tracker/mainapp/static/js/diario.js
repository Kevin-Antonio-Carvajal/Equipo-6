const elemento = document.getElementById('hola-mundo')        
elemento.addEventListener('click', () => {
    const id_habito = 16
    const url = elemento.getAttribute('data-url').replace('0', id_habito)
    // const token = getCookie("csrftoken")
    // console.log(token)
    const csrfToken = document.getElementById('csrf-token')
    // Realizar la solicitud AJAX para marcar las notificaciones como leídas
    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),  // Incluir el CSRF token si es necesario
            'Content-Type': 'application/json'
        },
        credentials: 'same-origin'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error en la respuesta del servidor');
        }
        return response.json();  // Esperar la respuesta como JSON
    })
    .then(data => {
        if (data.status === 'ok') {
            console.log('Notificaciones marcadas como leídas.');
        } else {
            console.error('Error en la respuesta:', data.message);
        }
    })
    .catch(error => console.error('Error en la solicitud AJAX:', error));
})

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}