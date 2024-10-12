from datetime import date
from django.utils import timezone
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .models import Categoria, Objetivo, Habito, Dia, Registro
from mainapp.context_processors import get_usuario
from django.db.models import Q

def index(request):

    return render(request, 'mainapp/index.html', {
        'titulo': 'Pagina de Inicio'
    })

def diario(request):

    # Obtenemos el usuario que inició sesión
    usuario_contexto = get_usuario(request)
    usuario = usuario_contexto.get('usuario')

    # Verificamos si hay un usuario autenticado
    if usuario:
        # Obtenemos los hábitos del usuario que se deben cumplir hoy
        habitos_hoy = obtener_habitos_hoy(usuario)
    else:
        habitos_hoy = []

    # Obtenemos los registros del día de hoy en una sola consulta
    hoy = date.today()
    registros_hoy = Registro.objects.filter(id_habito__in=habitos_hoy, fecha_creacion__date=hoy)

    habitos = []
    for habito in habitos_hoy:
        # Verificamos si el hábito tiene un registro creado hoy
        completado_hoy = registros_hoy.filter(id_habito=habito).exists()

        habitos.append({
            'id_habito': habito.id_habito,
            'objetivo': habito.id_objetivo,  # Ya es un objeto, no hace falta otra consulta
            'categoria': habito.id_categoria,  # Ya es un objeto, no hace falta otra consulta
            'nombre': habito.nombre,
            'frecuencia': habito.frecuencia,
            'completado': completado_hoy  # True si el hábito está completado hoy
        })

    contexto = {
        'titulo': 'Mantente al día',
        'habitos': habitos
    }

    return render(request, 'mainapp/diario.html', contexto)

def crear_habito(request):

    # Obtenemos todas las categorias
    categorias = Categoria.objects.all()

    return render(request, 'mainapp/crear_habito.html', {
        'titulo': 'Crear Nuevo Hábito',
        'categorias': categorias,
    })

def guardar_habito(request):

    # Obtenemos el usuario que inicio sesion
    usuario_contexto = get_usuario(request)
    usuario = usuario_contexto.get('usuario')

    if request.method == 'POST':
        id_usuario = usuario['id']
        nombre = request.POST['nombre']
        # Como el campo descripcion es opcional, en caso de que no se encuentre regresa ''
        descripcion = request.POST.get('descripcion', '')
        frecuencia = int(request.POST['frecuencia'])
        id_categoria = request.POST['categoria']
        tipo_objetivo = request.POST['objetivo']
        notificar = 'notificar' in request.POST 

        # Creamos un nuevo objetivo vinculado al hábito
        objetivo = Objetivo.objects.create(
            tipo=tipo_objetivo
        )
        
        # Creamos el habito
        habito = Habito.objects.create(
            id_usuario_id=id_usuario,
            id_objetivo=objetivo,
            id_categoria_id=id_categoria,
            nombre=nombre,
            descripcion=descripcion,
            frecuencia=frecuencia,
            notificar=notificar
        )
        # Guardamos los días si el objetivo es semanal o mensual
        if tipo_objetivo == 'semanal':
            dias_semana = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']                        
            for indice, dia in enumerate(dias_semana, start=1):
                # Si el checbox no fue seleccionado entonces no estara en el POST
                if dia in request.POST:
                    # Creamos el dia
                    Dia.objects.create(
                        id_objetivo=objetivo,
                        dia=indice
                    )
        elif tipo_objetivo == 'mensual':
            # Seleccionamos los dias del mes que el usuario eligio
            for indice in range(1,32):
                if f"dia-{indice}" in request.POST:
                    Dia.objects.create(
                        id_objetivo=objetivo,
                        dia=indice
                    )
        else:
            # El objetivo es diario
            pass
        # Mensajes de éxito
        contexto = {
            'mensaje_exitoso': 'Habito creado exitosamente'
        }
        # Redirigimos a la pantalla principal
        return render(request, 'mainapp/index.html', contexto)

def lista_habitos(request):
    habitos = Habito.objects.all()  # Recupera todos los hábitos de la base de datos
    return render(request, 'mainapp/lista_habitos.html', {'habitos': habitos})

# Vista para editar un hábito específico
def editar_habito(request, id_habito):
    habito = get_object_or_404(Habito, id_habito=id_habito)
    categorias = Categoria.objects.all()  # Obtén todas las categorías para el formulario

    if request.method == 'POST':
        habito.nombre = request.POST['nombre']
        habito.descripcion = request.POST.get('descripcion', '')
        habito.frecuencia = request.POST['frecuencia']
        habito.id_categoria_id = request.POST['categoria']
        habito.notificar = 'notificar' in request.POST
        habito.save()  # Guarda los cambios en la base de datos

        return redirect('lista_habitos')  # Redirige a la lista de hábitos después de editar

    return render(request, 'mainapp/editar_habito.html', {
        'habito': habito,
        'categorias': categorias,
    })

# Nueva vista para eliminar un hábito
def eliminar_habito(request, id_habito):
    habito = get_object_or_404(Habito, id_habito=id_habito)
    habito.delete()  # Elimina el hábito de la base de datos
    return redirect('lista_habitos')  # Redirige de nuevo a la lista de hábitos

def obtener_habitos_hoy(usuario):
    # Fecha actual
    hoy = date.today()  # Obtenemos la fecha de hoy
    dia_semana = hoy.weekday() + 1  # Dia de la semana (lunes es 0, domingo es 6, ajustamos a 1-7)
    dia_mes = hoy.day  # Obtenemos el día del mes (1 al 31)

    # Filtramos hábitos diarios
    filtro_diario = Q(id_objetivo__tipo='diario')

    # Filtramos hábitos semanales que coincidan con el día de la semana actual
    filtro_semanal = Q(id_objetivo__tipo='semanal') & Q(id_objetivo__dia__dia=dia_semana)

    # Filtramos hábitos mensuales que coincidan con el día del mes actual
    filtro_mensual = Q(id_objetivo__tipo='mensual') & Q(id_objetivo__dia__dia=dia_mes)

    # Unimos todos los filtros
    filtros = filtro_diario | filtro_semanal | filtro_mensual

    # Obtenemos todos los hábitos que cumplan con alguno de los filtros
    habitos_hoy = Habito.objects.filter(
        filtros,
        id_usuario=usuario['id'],
        estatus=True
    )

    return habitos_hoy

def completar_habito(request, id_habito):
    # Obtener el hábito correspondiente
    habito = Habito.objects.get(id_habito=id_habito)

    # Crear un nuevo registro relacionado con el hábito y la fecha actual (si no existe ya uno)
    if habito:
        # Verificamos si ya existe un registro relacionado al dia de hoy
        registro = Registro.objects.filter(
            id_habito=habito,
            fecha_creacion__date=timezone.now().date()  # Solo la parte de la fecha
        ).first()
        if registro:
            return HttpResponse('Ya existe un registro')
        else:
            Registro.objects.create(
                id_habito=habito
            )
            return redirect('diario')
    else:
        return HttpResponse('No existe el habito')    


def descompletar_habito(request, id_habito):
    # Obtener el hábito correspondiente
    habito = Habito.objects.get(id_habito=id_habito)

    if habito:
        # Eliminar el registro del día actual relacionado con el hábito
        registro = Registro.objects.filter(
            id_habito=habito,
            fecha_creacion__date=timezone.now().date()  # Solo la parte de la fecha
        ).first()

        if registro:
            registro.delete()
            return redirect('diario')
        else:
            return HttpResponse('No existe el registro')
    else:
        return HttpResponse('No existe el habito')    
    

    
    
    
