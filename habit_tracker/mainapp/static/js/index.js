/**
 * Grafica
 */
let progresoChart = null;

const start = () => {
    // Mostramos la grafica por default
    cargaGraficaDefault()    
    // Cargamos los filtros del mes
    cargaFiltroMes()
    // Cargamos el boton para eliminar los filtros
    cargaLimpiarFiltros()
}

const cargaLimpiarFiltros = () => {
    const span = document.createElement('span')
    span.innerText = "Limpiar"
    span.addEventListener('click', () => {
        // Limpiamos los filtros
        const categoria = document.getElementById('categoria')
        const mes = document.getElementById('mes')
        categoria.value = 0
        mes.value = `${new Date().getMonth() + 1}`
        cargaGraficaDefault()
    })
    // Contenedor
    const filtros = document.getElementById('filtros')
    filtros.appendChild(span)
}

const cargaFiltroMes = () => {
    const meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
    // Contenedor
    const div = document.createElement('div')
    // Label
    const label = document.createElement('label')
    label.setAttribute('for', 'mes')
    label.innerText = "Mes:"
    // Select
    const select = document.createElement('select')
    select.name = 'mes'
    select.id = 'mes'    
    // Options
    for (let i = 0 ; i < meses.length ; i++){
        const mes = meses[i]
        // Option
        const option = document.createElement('option')
        option.value = i+1
        option.innerText = mes
        const mesActual = new Date().getMonth()
        if (i == mesActual) {
            option.selected = true
        }
        select.appendChild(option)
    }    
    // Evento select
    select.addEventListener('change', filtrar)
    div.appendChild(label)
    div.appendChild(select)
    // Controladores
    const filtros = document.getElementById('filtros')    
    filtros.appendChild(div)    
}

const filtrar = (event) => {
    const categoria = document.getElementById('categoria').value
    const mes = document.getElementById('mes').value    
    // let url = document.getElementById('filtrar-progreso-accion').getAttribute('data-url')
    let url = `/filtrar_progreso/${categoria}/${mes}/`
    const csrftoken = getCookie('csrftoken')
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
        // Actualizamos el grafico
        actualizarGrafico(data.dias, data.progreso);
    })
    .catch(error => console.error('Error al completar el hábito:', error));
}

const actualizarGrafico = (dias, progreso) => {
    const ctx = document.getElementById('grafica').getContext('2d');
    crearGraficaProgreso(ctx, dias, progreso);
}

const crearGraficaProgreso = (ctx, dias, progreso) => {
    // Si ya existe un gráfico, lo destruimos para evitar superposiciones
    if (progresoChart) {
        progresoChart.destroy();
    }

    // Crear el gráfico con Chart.js
    progresoChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: dias,  // Los días del mes
            datasets: [{
                label: 'Progreso Acumulado',
                data: progreso,  // El progreso por día
                borderColor: 'rgba(33, 150, 243, 1)',
                backgroundColor: 'rgba(33, 150, 243, 0.2)',
                fill: true,
                borderWidth: 2,
                tension: 0.2,  // Suavizar la curva
                pointRadius: 4,  // Tamaño de los puntos
                pointBackgroundColor: 'rgba(33, 150, 243, 1)',  // Color de los puntos
            }]
        },
        options: {
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Día del Mes'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Hábitos Cumplidos'
                    },
                    beginAtZero: true
                }
            }
        }
    });
}

const cargaGraficaDefault = () => {
    // Al cargar el componente, mostramos la grafica de progreso
    const dias = JSON.parse(document.getElementById('data-dias').getAttribute('data-dias'));
    const progreso = JSON.parse(document.getElementById('data-progreso').getAttribute('data-progreso'));
    const ctx = document.getElementById('grafica').getContext('2d');
    crearGraficaProgreso(ctx, dias, progreso)
}

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

start()