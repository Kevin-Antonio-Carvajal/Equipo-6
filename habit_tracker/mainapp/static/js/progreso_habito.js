document.addEventListener('DOMContentLoaded', function() {
    // Obtener los datos del contexto de Django
    const completado = parseInt(document.getElementById('data-completado').getAttribute('data-completado'));
    const restante = parseInt(document.getElementById('data-restante').getAttribute('data-restante'));

    // Datos para la gráfica circular
    const data = {
        labels: ['Completado', 'Restante'],
        datasets: [{
            data: [completado, restante],
            backgroundColor: [
                'rgba(33, 150, 243, 0.6)',  // Color para completado
                'rgba(201, 203, 207, 0.6)'  // Color para restante
            ],
            borderColor: [
                'rgba(33, 150, 243, 1)',
                'rgba(201, 203, 207, 1)'
            ],
            borderWidth: 1
        }]
    };

    // Opciones para la gráfica circular
    const opciones = {
        responsive: true,
        plugins: {
            legend: {
                position: 'bottom',
                labels: {
                    font: {
                        size: 10  // Ajusta el tamaño del texto de las leyendas aquí
                    }
                }
            },
            title: {
                display: true,
                // text: 'Progreso del Hábito'
            }
        },
        cutout: '80%'
    };

    // Crear la gráfica circular
    const ctx = document.getElementById('graficaCircular').getContext('2d');
    const graficaCircular = new Chart(ctx, {
        type: 'doughnut',  // Puedes usar 'pie' si prefieres
        data: data,
        options: opciones
    });
});

/**
 * Regresa a la pagina anterior
 */
const backPage = () => {
    // Regresamos a la pagina anterior
    window.history.back();
}