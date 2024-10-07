const start = () => {
    
}

// Funcion para cerrar el modal para seleccionar una categoria
const closeModalSeleccionaCategoria = (event) => {
    // Modal
    const modal = document.getElementById('modal-selecciona-categoria')
    modal.style.display = 'none'
}

// Funcion para abrir el modal para seleccionar una categoria
const openModalSeleccionaCategoria = (event) => {
    // Modal
    const modal = document.getElementById('modal-selecciona-categoria')
    modal.style.display = 'flex'
}

// Funcion para cuando se da click en una etiqueta en el panel de agregar etiquetas
const clickEtiquetaDisponible = (event) => {
    // Categoria seleccionada
    const categoria = event.currentTarget
    // Contenedor al que vamos a agregarlo
    const contenedorCategorias = document.getElementById('categorias')
    // Lo agregamos al contenedor de categorias
    contenedorCategorias.appendChild(categoria)

}

// Al ejecutarse el componente
start()

