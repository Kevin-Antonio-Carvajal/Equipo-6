from django.shortcuts import render, HttpResponse
from .models import Categoria
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

    informacion = None

    if request.method == 'GET':
        pass

    return HttpResponse(f"<h2>Habito guardado: {informacion}</h2>")