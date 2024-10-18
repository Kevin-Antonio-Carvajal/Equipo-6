from .models import Notificacion

# Contexto que regresa el usuario que inicio la sesion
def get_usuario(request):
    usuario = None
    # Verificamos si hay información del usuario en la sesión
    if 'usuario_id' in request.session:
        usuario = {
            'id': request.session.get('usuario_id'),
            'nombre': request.session.get('usuario_nombre'),
            'correo': request.session.get('usuario_correo'),
            'username': request.session.get('usuario_username'),
        }

    return {
        'usuario': usuario
    }

def obtener_notificaciones(request):
    usuario_contexto = get_usuario(request)
    usuario = usuario_contexto.get('usuario')

    if usuario:
        usuario = usuario['id']
        notificaciones = Notificacion.objects.filter(id_habito__id_usuario=usuario, estatus=False)
        notificaciones_no_leidas = notificaciones.count()
    else:
        notificaciones = []
        notificaciones_no_leidas = 0

    return {
        'notificaciones': notificaciones,
        'notificaciones_no_leidas': notificaciones_no_leidas,
    }
