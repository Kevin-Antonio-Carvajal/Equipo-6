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
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                fill: true,
                borderWidth: 2,
                tension: 0.2,  // Suavizar la curva
                pointRadius: 4,  // Tamaño de los puntos
                pointBackgroundColor: 'rgba(75, 192, 192, 1)',  // Color de los puntos
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

// Llamar la función para iniciar la gráfica
start();
