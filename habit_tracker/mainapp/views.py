from django.shortcuts import render, HttpResponse, redirect
from .models import Categoria, Objetivo, Habito, Dia
from mainapp.context_processors import get_usuario

def index(request):

    return render(request, 'mainapp/index.html', {
        'titulo': 'Pagina de Inicio'
    })

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
            id_objetivo_id=objetivo.id_objetivo,
            id_categoria_id=id_categoria,
            nombre=nombre,
            descripcion=descripcion,
            frecuencia=frecuencia,
            notificar=notificar
        )
        # Guardamos los días si el objetivo es semanal o mensual
        if objetivo == 'semanal':
            dias_semana = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']                        
            for indice, dia in enumerate(dias_semana, start=1):
                # Si el checbox no fue seleccionado entonces no estara en el POST
                if dia in request.POST:
                    # Creamos el dia
                    Dia.objects.create(
                        id_objetivo_id=objetivo.id_objetivo,
                        dia=indice
                    )
        elif objetivo == 'mensual':
            # Seleccionamos los dias del mes que el usuario eligio
            for indice in range(1,32):
                if f"dia-{indice}" in request.POST:
                    Dia.objects.create(
                        id_objetivo_id=objetivo.id_objetivo,
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
    