from django.shortcuts import render, HttpResponse
from .models import Categoria, Categorizado
from mainapp.context_processors import get_usuario

def index(request):

    return render(request, 'mainapp/index.html', {
        'titulo': 'Pagina de Inicio'
    })

def crear_habito(request):

    # Obtenemos todas las categorias
    categorias_todas = Categoria.objects.all()

    # Obtenemos el contexto del usuario que inicio sesion
    usuario_contexto = get_usuario(request)
    usuario = usuario_contexto['usuario']

    # Obtener las categorías relacionadas a los hábitos del usuario
    categorias_usuario = Categoria.objects.filter(
        id_categoria__in = Categorizado.objects.filter(
            id_habito__id_usuario=usuario['id'] # Filtrar hábitos por usuario
        ).values('id_categoria') # Obtener solo los ids de las categorías
    ).distinct() # Usamos distinct() para evitar duplicados si un usuario tiene varios hábitos con la misma categoría

    # Unir todas las categorías disponibles con las categorías relacionadas con el usuario
    # Esto eliminará duplicados entre las dos consultas
    categorias = categorias_todas.union(categorias_usuario)

    return render(request, 'mainapp/crear_habito.html', {
        'titulo': 'Crear Nuevo Hábito',
        'categorias': categorias,
    })

def guardar_habito(request):

    informacion = None

    if request.method == 'GET':
        pass

    return HttpResponse(f"<h2>Habito guardado: {informacion}</h2>")