/**
 * Referencias que se utilizaron para poder hacer un fetch desde un archivo .js:
 * 
 * Como usar fetch en .js:
 * https://stackoverflow.com/questions/71268023/how-to-correctly-use-fetch-in-javascript-and-django
 * 
 * Como incrustar un parametro a una url en django desde .js:
 * https://stackoverflow.com/questions/68707195/url-to-fetch-with-parameter-for-django-view
 * 
 * Como pasar el token CSRF a un archivo .js:
 * https://stackoverflow.com/questions/23349883/how-to-pass-csrf-token-to-javascript-file-in-django
 * 
 * Como obtener el token CSRF desde un archivo .js:
 * https://stackoverflow.com/questions/16209959/how-can-i-embed-a-csrf-token-in-a-javascript-file
 * 
 * Como acceder al token CSRF en el backend:
 * https://stackoverflow.com/questions/65857621/how-to-access-the-csrf-token-inside-django-view
 */

/**
 * Funcion que se dispara al querer marcar/desmarcar un habito
 * @param {*} event evento disparado
 * @param {*} id_habito id del habito
 */
const toggle = (event, id_habito) => {
    // Obtener el elemento que disparó el evento
    const elemento = event.currentTarget;
    // Verificar si el elemento tiene la clase 'active'
    if (elemento.classList.contains('active')) {        
        descompletar_habito(id_habito, elemento)
    } else {
        completar_habito(id_habito, elemento)
    }    
}
/**
 * Completa un habito
 * @param {*} id_habito id del habito
 * @param {*} elemento elemento que disparo el evento
 */
const completar_habito = (id_habito, elemento) => {
    const csrftoken = getCookie('csrftoken')
    const url = `/completar_habito/${id_habito}/`
    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json'
        },
        credentials: 'same-origin'
    })
    .then(response => response.json())
    .then(data => {
        if (data.completado) {
            elemento.classList.add('active');
            actualizarNotificaciones(); // Llama a la actualización de notificaciones
        }
    })
    .catch(error => console.error('Error al completar el hábito:', error));
};

/**
 * Descompleta un habito
 * @param {*} id_habito id del habito
 * @param {*} elemento elemento que disparo el evento
 */
const descompletar_habito = (id_habito, elemento) => {
    const csrftoken = getCookie('csrftoken')
    const url = `/descompletar_habito/${id_habito}/`
    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json'
        },
        credentials: 'same-origin'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error en la respuesta del servidor');
        }
        return response.json();
    })
    .then(data => {
        if (data.descompletado) {
            elemento.classList.remove('active');
            actualizarNotificaciones(); // Llama a la actualización de notificaciones
        }
    })
    .catch(error => console.error('Error al descompletar el hábito:', error));
};

/**
 * Funcion que regresa una Cookie
 * @param {*} name nombre de la cookie
 * @returns 
 */
const getCookie = (name) => {
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

/**
 * Redirige a la pagina para editar un habito
 * @param {*} event evento disparado
 * @param {*} id_habito id del habito
 */
const editarHabito = (event, id_habito) => {
    window.location.href = `/editar_habito/${id_habito}`
}

/**
 * Redirige a la pagina para ver el progreso de un habito
 * @param {*} event evento disparado
 * @param {*} id_habito id del habito
 */
const progresoHabito = (event, id_habito) => {
    window.location.href = `/progreso_habito/${id_habito}`
}

/**
 * Regresa a la pagina anterior
 */
const backPage = () => {
    // Regresamos a la pagina anterior
    window.history.back();
}

// Llama a esta función cada vez que se complete o descomplete un hábito
function actualizarNotificaciones() {
    fetch('/obtener_notificaciones/')
        .then(response => response.json())
        .then(data => {
            const notificationContent = document.getElementById('notification-content');
            notificationContent.innerHTML = ''; // Limpia las notificaciones actuales

            // Si hay notificaciones pendientes, mostrar
            if (data.notificaciones.length > 0) {
                data.notificaciones.forEach(notificacion => {
                    const notificationItem = document.createElement('div');
                    notificationItem.classList.add('notification-item');
                    notificationItem.innerHTML = `<strong>${notificacion.titulo}</strong><br>${notificacion.descripcion}<br><em>${notificacion.mensaje_motivacional}</em>`;
                    notificationContent.appendChild(notificationItem);
                });
            } else if (data.mensaje_felicitacion) {
                // Si no hay notificaciones, mostrar mensaje de felicitación
                const felicitationItem = document.createElement('div');
                felicitationItem.classList.add('notification-item');
                felicitationItem.innerText = data.mensaje_felicitacion;
                notificationContent.appendChild(felicitationItem);
            }

            // Actualiza el contador de notificaciones
            const badge = document.querySelector('.badge');
            badge.innerText = data.notificaciones_no_leidas;
        })
        .catch(error => console.error('Error al obtener notificaciones:', error));
}




