const backPage = () => {
    // Regresamos a la pagina anterior
    window.history.back();
}

const completarToggle = (event, id_habito) => {
    // Obtener el elemento que disparó el evento
    const elemento = event.currentTarget;    
    // Verificar si el elemento tiene la clase 'active'
    if (elemento.classList.contains('active')) {        
        // Eliminamos el registro con el dia de hoy
        window.location.replace(`/descompletar_habito/${id_habito}`);
    } else {
        console.log('completar habito')
        // Creamos un registro con el dia de hoy        
        window.location.replace(`/completar_habito/${id_habito}`);
    }    
}

const editarHabito = (event, id_habito) => {
    window.location.href = `/editar_habito/${id_habito}`
}