const start = () => {
    // Inicializar el selector de fechas cuando el DOM esté completamente cargado
    $(document).ready(function() {
        $('.date').datepicker({
            multidate: true,      // Permitir seleccionar múltiples fechas
            format: 'dd-mm-yyyy', // Formato de las fechas
            todayHighlight: true, // Resaltar la fecha actual
            autoclose: true       // Cerrar el selector automáticamente al hacer clic fuera
        });
    });
}

const clickcito = (event) => {
    console.log('Hola mundo!')
}

// Al ejecutarse el componente
start()

