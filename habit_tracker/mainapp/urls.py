from django.urls import path
from . import views

urlpatterns = [
    path(
        '',             # Ruta
        views.index,    # Vista
        name='inicio'   # Nombre
    ),
    path(
        'inicio/',
        views.index,
        name='index'
    ),
    path(
        'crear-habito/',
        views.crear_habito,
        name='crear_habito'
    )
]