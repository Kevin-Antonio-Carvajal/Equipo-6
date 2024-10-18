const start = () => {
    // Agregamos un evento al formulario
    document.getElementById('formulario-habito').addEventListener('submit', verificaFormulario)
}

const verificaFormulario = (event) => {
    // Detenemos el envio
    event.preventDefault()
    // Verificamos que si selecciono objetivo semanal o mensual por lo menos haya un checkbox activo
    const radioDiario = document.getElementById('diario')
    if (!radioDiario.checked){
        const objetivoDiasContenedor = document.getElementById('objetivo-dias-contenedor')
        const checkboxes = objetivoDiasContenedor.getElementsByTagName('input')        
        if (!almenosUnCheckboxSeleccionado(checkboxes)){
            // Mostramos error al usuario
            const error = document.createElement('p')
            error.innerHTML = "Selecciona al menos un día"
            error.className = 'error'
            objetivoDiasContenedor.appendChild(error)
            return
        }
    }
    // Continuamos con el envio
    event.target.submit()

}

const almenosUnCheckboxSeleccionado = (checkboxes) => {
    for (let checkbox of checkboxes){
        if (checkbox.checked){
            return true       
        }
    }
    return false
}

const agregaDiasMes = () => {
    eliminaDias()
    // Contenedor
    const contenedor = document.getElementById('objetivo-dias-contenedor')
    // Dias del mes
    const diasMes = document.createElement('div')
    diasMes.id = 'dias-mes'
    // Dias del mes
    for (let i = 1; i < 32 ; i++){
        const dia = crearDiaMes(i)
        diasMes.appendChild(dia)
    }
    // Agregamos al contenedor
    contenedor.appendChild(diasMes)
}

const agregaDiasSemana = () => {
    eliminaDias()
    // Contenedor
    const contenedor = document.getElementById('objetivo-dias-contenedor')
    // Dias de la semana
    const diasSemana = document.createElement('div')
    diasSemana.id = 'dias-semana'
    // Dias de la semana
    for (let nombre of ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']){
        const dia = crearDiaSemana(nombre)
        diasSemana.appendChild(dia)
    }
    // Agregamos al contenedor
    contenedor.appendChild(diasSemana)
}

const eliminaDias = () => {
    document.getElementById('objetivo-dias-contenedor').replaceChildren()
}

const crearDiaMes = (numero) => {
    // Contenedor
    const div = document.createElement('div')
    div.className = 'tile'
    // Checkbox
    const checkbox = document.createElement('input')
    checkbox.type = "checkbox"
    checkbox.id = `dia-${numero}`
    checkbox.name = `dia-${numero}`
    // Verificamos si el numero corresponde al dia de hoy
    const hoy = new Date()
    const diaHoy = hoy.getDate()
    if (diaHoy === numero){
        checkbox.checked = true
    }
    // Label
    const label = document.createElement('label')
    label.htmlFor = `dia-${numero}`
    label.textContent = numero
    // Agregamos al contenedor
    div.appendChild(checkbox)
    div.appendChild(label)

    return div
}

const crearDiaSemana = (nombre) => {
    // Contenedor
    const div = document.createElement('div')
    div.className = 'tile-semana'
    // Checkbox
    const checkbox = document.createElement('input')
    checkbox.type = 'checkbox'
    checkbox.id = nombre
    checkbox.name = nombre
    // Verificamos si el nombre coincide con el dia de hoy
    const diasSemana = ['domingo', 'lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado']
    const hoy = new Date()
    const diaHoy = diasSemana[hoy.getDay()]
    if (diaHoy === nombre){
        checkbox.checked = true
    }        
    // Label
    const label = document.createElement('label')
    label.htmlFor = nombre
    label.textContent = nombre
    // Agregamos al contenedor
    div.appendChild(checkbox)
    div.appendChild(label)
    return div
}

const backPage = () => {
    // Regresamos a la pagina anterior
    window.history.back();
}


// Al ejecutarse el componente
start()

