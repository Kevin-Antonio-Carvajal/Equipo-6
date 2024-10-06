from django.shortcuts import render

def index(request):

    return render(request, 'mainapp/index.html', {
        'titulo': 'Pagina de Inicio'
    })

def crear_habito(request):

    return render(request, 'mainapp/crear_habito.html', {
        'titulo': 'Crear Hábito'
    })
