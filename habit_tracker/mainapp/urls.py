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
        'crear_habito/',
        views.crear_habito,
        name='crear_habito'
    ),
    path(
        'guardar_habito/',
        views.guardar_habito,
        name='guardar_habito'
    )
]