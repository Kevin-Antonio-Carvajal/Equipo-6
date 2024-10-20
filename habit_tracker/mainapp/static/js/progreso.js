const start = () => {
    // Al cargar el componente, obtenemos los datos
    const dias = JSON.parse(document.getElementById('data-dias').getAttribute('data-dias'));
    const progreso = JSON.parse(document.getElementById('data-progreso').getAttribute('data-progreso'));

    const ctx = document.getElementById('grafica').getContext('2d');
    
    // Crear la gráfica de progreso
    const progresoChart = new Chart(ctx, {
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
};

/**
 * Redirige a la pagina para ver el progreso de un habito
 * @param {*} event evento disparado
 * @param {*} id_habito id del habito
 */
const progresoHabito = (event, id_habito) => {
    window.location.href = `/progreso_habito/${id_habito}`
}

// Llamar la función para iniciar la gráfica
start();
