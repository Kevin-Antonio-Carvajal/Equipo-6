
# Contexto que regresa el usuario que inicio la sesion
def get_usuario(request):

    usuario = {
        'id': 1,
        'nombre': 'Luis Sebastian',
        'correo': 'sebastian_luis@ciencias.unam.mx',
        'username': 'sebsDev'
    }

    return {
        'usuario': usuario
    }