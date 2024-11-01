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
        'diario/', 
        views.diario, 
        name='diario'
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
    ),
    path(
        'lista_habitos/', 
        views.lista_habitos, 
        name='lista_habitos'
    ), 
    path(
        'editar_habito/<int:id_habito>/', 
        views.editar_habito, 
        name='editar_habito'
    ),
    path(
        'eliminar_habito/<int:id_habito>/', 
        views.eliminar_habito, 
        name='eliminar_habito'
    ),
    path(
        'completar_habito/<int:id_habito>/',
        views.completar_habito,
        name='completar_habito'        
    ),
    path(
        'descompletar_habito/<int:id_habito>/',
        views.descompletar_habito,
        name='descompletar_habito'
    ),
    #Rutas del login y register, aun no se si es que aqui esta el error
    path(
        'login/', 
        views.login_view,
        name='login'
    ),
    path(
        'register/', 
        views.register, 
        name='register'
    ), 
    path('logout/',
        views.logout_view, 
        name='logout'),

    path(
        'obtener_notificaciones/',
        views.obtener_notificaciones,
        name='obtener_notificaciones'
    ),
    path(
        'progreso/',
        views.progreso,
        name='progreso'
    ),
    path(
        'progreso_habito/<int:id_habito>/',
        views.progreso_habito,
        name='progreso_habito'
    ),
    path(
        'filtrar_progreso/<int:categoria>/<int:mes>/',
        views.filtrar_progreso,
        name='filtrar_progreso'
    ),
    path(
        'editar_recordatorio/<int:id_notificacion>/', 
        views.editar_recordatorio, 
        name='editar_recordatorio'
    ),
    path(
        'editar_perfil/', 
        views.editar_perfil, 
        name='editar_perfil'
    ) 
]