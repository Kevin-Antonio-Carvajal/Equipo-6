import calendar
import matplotlib.pyplot as plt
from datetime import date
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .models import Categoria, Objetivo, Habito, Dia, Registro, Usuario
from mainapp.context_processors import get_usuario
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from mainapp.forms import FormRegister
from mainapp.CryptoUtils import cipher, sha256, decipher, validate
from django.db import models
from .models import Notificacion
from .forms import NotificacionForm

def obtener_habitos_no_completados(usuario):
    hoy = timezone.now().date()
    habitos_hoy = obtener_habitos_hoy(usuario)
    
    # Obtener registros de hábitos completados hoy
    habitos_completados_hoy = Registro.objects.filter(
        id_habito__in=habitos_hoy, 
        fecha_creacion__date=hoy
    ).values_list('id_habito', flat=True)
    
    # Filtrar los hábitos de hoy que no están completados
    habitos_no_completados = habitos_hoy.exclude(id_habito__in=habitos_completados_hoy)
    
    return habitos_no_completados

class NotificacionGlobal(models.Model):
    mensaje = models.CharField(max_length=255)
    fecha_envio = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)  # Permitir activar o desactivar notificaciones

def index(request):

    return render(request, 'mainapp/index.html', {
        'titulo': 'Pagina de Inicio'
    })

def diario(request):
    usuario_contexto = get_usuario(request)
    usuario = usuario_contexto.get('usuario')

    if usuario is None:
        messages.error(request, 'Debes iniciar sesión para ver tu diario.')
        return redirect('login')

    habitos_hoy = obtener_habitos_hoy(usuario)
    hoy = timezone.now().date()
    registros_hoy = Registro.objects.filter(
        id_habito__in=habitos_hoy,
        fecha_creacion__date=hoy
    ).values_list('id_habito', flat=True)

    habitos = []
    notificaciones = []
    
    for habito in habitos_hoy:
        completado = habito.id_habito in registros_hoy
        habitos.append({
            'id_habito': habito.id_habito,
            'categoria': habito.id_categoria,
            'nombre': habito.nombre,
            'frecuencia': habito.frecuencia,
            'completado': completado
        })
        
        if not completado:
            notificacion, created = Notificacion.objects.get_or_create(
                id_habito=habito,
                estatus=False,
                defaults={
                    'titulo': f"Recuerda que no has completado el habito '{habito.nombre}' hoy.",
                    'descripcion': f"No has completado el hábito '{habito.nombre}' hoy.",
                    'mensaje_motivacional': "¡No te rindas, continúa con tu rutina!"
                }
            )
            notificaciones.append(notificacion)
    
    contexto = {
        'titulo': 'Mantente al día',
        'habitos': habitos,
        'notificaciones': notificaciones,
        'notificaciones_no_leidas': len(notificaciones),
    }

    return render(request, 'mainapp/diario.html', contexto)

def crear_habito(request):

    # Obtenemos el usuario que inicio sesion
    usuario_contexto = get_usuario(request)
    usuario = usuario_contexto.get('usuario')

    if usuario is None:
        # Si no hay un usuario en la sesión, redirigir al inicio de sesión
        messages.error(request, 'Debes iniciar sesión para crear un hábito.')
        return redirect('login')

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

    if usuario is None:
        # Si no hay un usuario en la sesión, redirigir al inicio de sesión
        messages.error(request, 'Debes iniciar sesión para crear un hábito.')
        return redirect('login')

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
        messages.success(request, 'Habito creado exitosamente')
        # Redirigimos a la pantalla principal
        return redirect('diario')
    else:
        return redirect('index')

def lista_habitos(request):

    # Obtenemos el usuario que inicio sesion
    usuario_contexto = get_usuario(request)
    usuario = usuario_contexto.get('usuario')

    if usuario is None:
        # Si no hay un usuario en la sesión, redirigir al inicio de sesión
        messages.error(request, 'Debes iniciar sesión para ver todos tus habitos')
        return redirect('login')
    

    habitos = Habito.objects.filter(id_usuario_id=usuario['id'])  # Recupera todos los hábitos de la base de datos
    return render(request, 'mainapp/lista_habitos.html', {'habitos': habitos})

# Vista para editar un hábito específico
def editar_habito(request, id_habito):
    habito = get_object_or_404(Habito, id_habito=id_habito)
    categorias = Categoria.objects.all()
    dias = Dia.objects.filter(id_objetivo=habito.id_objetivo)
    
    if request.method == 'POST':
        # Actualizar los campos del hábito
        habito.nombre = request.POST['nombre']
        habito.descripcion = request.POST.get('descripcion', '')
        habito.frecuencia = request.POST['frecuencia']
        habito.id_categoria_id = request.POST['categoria']
        habito.notificar = 'notificar' in request.POST
        
        # Actualizar el objetivo
        habito.id_objetivo.tipo = request.POST['objetivo']
        habito.id_objetivo.save()

        # Eliminar los días existentes y añadir los nuevos si es necesario
        Dia.objects.filter(id_objetivo=habito.id_objetivo).delete()
        if habito.id_objetivo.tipo == 'semanal':
            for i, dia in enumerate(['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo'], start=1):
                if dia in request.POST:
                    Dia.objects.create(id_objetivo=habito.id_objetivo, dia=i)
        elif habito.id_objetivo.tipo == 'mensual':
            for i in range(1, 32):
                if f"dia-{i}" in request.POST:
                    Dia.objects.create(id_objetivo=habito.id_objetivo, dia=i)
        
        habito.save()
        return redirect('lista_habitos')
    
    return render(request, 'mainapp/editar_habito.html', {
        'habito': habito,
        'categorias': categorias,
        'dias': dias,
        'titulo': 'Editar Hábito'
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
    # Verificamos que el metodo sea POST
    if request.method == 'POST':
        try:
            # Obtener el hábito correspondiente
            habito = Habito.objects.get(id_habito=id_habito)
            # Verificamos si ya existe un registro relacionado al dia de hoy
            registro = Registro.objects.filter(
                id_habito=habito,
                fecha_creacion__date=timezone.now().date()  # Solo la parte de la fecha
            ).first()
            if registro:
                Notificacion.objects.filter(id_habito=habito, estatus=False).delete()
                return JsonResponse({
                    'message': 'Esta habito ya habia sido completado',
                    'compleado': True
                }, status=200)
            else:                
                Registro.objects.create(
                    id_habito=habito
                )
                return JsonResponse({
                    'message': 'Habito completado',
                    'completado': True
                }, status=200)
        except Habito.DoesNotExist:
            return JsonResponse({
                'error': 'No existe el habito'
            }, status=404)
    else:
        return JsonResponse({
            'error': 'Peticion invalida'
        }, status=400)

def descompletar_habito(request, id_habito):
    # Verificamos que el metodo sea POST
    if request.method == 'POST':
        try:
            # Obtener el hábito correspondiente
            habito = Habito.objects.get(id_habito=id_habito)
            # Obtenemos el registro relacionado a este habito
            registro = Registro.objects.filter(
                id_habito=habito,
                fecha_creacion__date=timezone.now().date()  # Solo la parte de la fecha
            ).first()
            if registro:
                registro.delete()
                # Creamos la notificacion
                Notificacion.objects.update_or_create(
                    id_habito=habito,
                    estatus=False,
                    defaults={
                        'titulo': f"Recordatorio para {habito.nombre}",
                        'descripcion': f"No has completado el hábito '{habito.nombre}' hoy.",
                        'mensaje_motivacional': "¡No te rindas, continúa con tu rutina!"
                    }
                )
                return JsonResponse({
                    'message': 'Habito descompletado',
                    'descompletado': True
                },status=200)
            else:
                return JsonResponse({
                    'message': 'Este habito no habia sido completado',
                    'descompletado': True
                },status=200)
        except Habito.DoesNotExist:
            return JsonResponse({
                'error': 'No existe el habito'
            },status=404)
    else:
        return JsonResponse({
            'error': 'Peticion invalida'
        },status=400)

# Esta función maneja el registro de nuevos usuarios, mostrando el formulario de registro y procesando la creación del usuario.
def register(request):
    
    if request.method == 'POST':
        formulario = FormRegister(request.POST)
        if formulario.is_valid():
            data_form = formulario.cleaned_data
            nombre = data_form.get('nombre')
            correo = data_form.get('correo')
            username = data_form.get('username')            
            password = data_form.get('password')
            # Varificamos si el correo no ha sido registrado
            existe_usuario = Usuario.objects.filter(correo=correo).exists()
            if existe_usuario:
                messages.error(request, f'Este correo electrónico ya está registrado. Si ya tienes una cuenta, por favor inicia sesión.')
                return redirect('register')
            else:
                # Registramos el usuario
                hashed_password = sha256(cipher(password)).hexdigest()
                usuario = Usuario.objects.create(
                    nombre=nombre,
                    correo=correo,
                    username=username,
                    password=hashed_password
                )
                messages.success(request, 'Te has registrado correctamente')
                return redirect('index')
    else:
        return render(request, 'mainapp/register.html', {'form': FormRegister()})

# Esta función maneja el inicio de sesión de los usuarios, autenticándolos y redirigiéndolos si las credenciales son correctas.
def login_view(request):
    if request.method == 'POST':
        correo = request.POST['username']
        password = request.POST['password']
        exite_usuario = Usuario.objects.filter(correo=correo).exists()
        if not exite_usuario:
            messages.error(request, 'Correo incorrecto')
            return redirect('login')
        else:
            usuario = Usuario.objects.get(correo=correo)
            if validate(password,usuario.password):
                # Guardamos la informacion del usuario en la sesion
                request.session['usuario_id'] = usuario.id_usuario
                request.session['usuario_nombre'] = usuario.nombre
                request.session['usuario_correo'] = usuario.correo
                request.session['usuario_username'] = usuario.username
                messages.success(request, f'Bienvenido, {usuario.nombre}!')
                return redirect('index')
            else:
                messages.error(request, 'Contraseña incorrecta')
                return redirect('login')
    else:
        return render(request, 'mainapp/login.html')
    

# Esta función maneja el cierre de sesión del usuario, redirigiéndolo al formulario de login.
def logout_view(request):
    # Limpiamos toda la información almacenada en la sesión
    request.session.flush()
    # Mostramos un mensaje de éxito al cerrar sesión
    messages.success(request, 'Has cerrado sesión exitosamente.')
    # Redirigimos al usuario a la página de inicio de sesión
    return redirect('login')

def obtener_notificaciones(request):
    # Obtener el usuario desde el contexto
    usuario_contexto = get_usuario(request)
    usuario = usuario_contexto.get('usuario')

    if usuario is None:
        # Si no está autenticado, devolver un error JSON
        return JsonResponse({'error': 'Usuario no autenticado'}, status=401)

    # Obtener hábitos no completados por el usuario
    habitos_no_completados = obtener_habitos_no_completados(usuario)
    notificaciones = Notificacion.objects.filter(id_habito__in=habitos_no_completados, estatus=False)

    # Si no hay notificaciones, devolver un mensaje de felicitación
    if not notificaciones.exists():
        return JsonResponse({
            'notificaciones': [],  # No hay notificaciones pendientes
            'notificaciones_no_leidas': 0,
            'mensaje_felicitacion': '¡Felicitaciones! Has completado todos tus hábitos hoy.'
        })

    # Si hay notificaciones, preparar los datos para devolver en formato JSON
    notificaciones_data = [{
        'id_notificacion': n.id_notificacion,  
        'titulo': n.titulo,
        'descripcion': n.descripcion,
        'mensaje_motivacional': n.mensaje_motivacional
    } for n in notificaciones]

    # Devolver las notificaciones junto con el número de no leídas
    return JsonResponse({
        'notificaciones': notificaciones_data,
        'notificaciones_no_leidas': len(notificaciones_data)
    })


def progreso(request):

    # Obtenemos el usuario que inicio sesion
    usuario_contexto = get_usuario(request)
    usuario = usuario_contexto.get('usuario')

    if usuario is None:
        # Si no hay un usuario en la sesión, redirigir al inicio de sesión
        messages.error(request, 'Debes iniciar sesión para obtener informacion de tu progreso.')
        return redirect('login')
    
    usuario = Usuario.objects.get(id_usuario=usuario['id'])
    habitos = Habito.objects.filter(id_usuario=usuario)

    fecha_actual = timezone.now()
    primer_dia, ultimo_dia = calendar.monthrange(fecha_actual.year, fecha_actual.month)

    # Diccionario para almacenar el progreso por día
    progreso_acumulativo = {}

    # Inicializamos el progreso en cero para cada día del mes
    for dia in range(1, ultimo_dia + 1):
        progreso_acumulativo[dia] = 0

    # Iteramos sobre los hábitos del usuario
    for habito in habitos:
        # Filtramos los registros del mes actual para cada hábito
        registros = Registro.objects.filter(
            id_habito=habito, 
            fecha_creacion__year=fecha_actual.year,
            fecha_creacion__month=fecha_actual.month
        )
        # Actualizamos el progreso acumulativo por cada registro
        for registro in registros:
            dia = registro.fecha_creacion.day
            progreso_acumulativo[dia] += 1

    # Categorias relacionadas a los habitos del usuario
    categorias = Categoria.objects.filter(habito__id_usuario=usuario).distinct()

    contexto = {
        'titulo': 'Mi Progreso',
        'dias': list(progreso_acumulativo.keys()),
        'progreso': list(progreso_acumulativo.values()),
        'habitos': habitos,
        'categorias': categorias
    }

    return render(request, 'mainapp/progreso.html', contexto)

def progreso_habito(request, id_habito):

     # Obtenemos el usuario que inicio sesion
    usuario_contexto = get_usuario(request)
    usuario = usuario_contexto.get('usuario')

    if usuario is None:
        # Si no hay un usuario en la sesión, redirigir al inicio de sesión
        messages.error(request, 'Debes iniciar sesión para obtener informacion del progreso de un habito')
        return redirect('login')

    if request.method == 'GET':
        habito = None
        try:
            habito = Habito.objects.get(id_habito=id_habito)
        except Habito.DoesNotExist:
            messages.error(request, 'No existe habito con ese ID')
            redirect('progreso')
        
        # Fecha actual y últimos días del mes
        fecha_actual = timezone.now()
        _, ultimo_dia = calendar.monthrange(fecha_actual.year, fecha_actual.month)

        # Obtener el tipo de objetivo del hábito
        tipo_objetivo = habito.id_objetivo.tipo

        # Calcular el total esperado basado en el tipo de objetivo
        if tipo_objetivo == 'diario':
            total_esperado = ultimo_dia
        elif tipo_objetivo == 'semanal':
            total_semanas = (ultimo_dia + fecha_actual.weekday()) // 7 + 1
            total_esperado = total_semanas
        elif tipo_objetivo == 'mensual':
            total_esperado = 1
        else:
            total_esperado = 0  # Manejar casos no definidos

        racha_actual, racha_maxima = obtener_rachas(habito)

        # Contar los registros completados en el mes actual
        registros_completados = Registro.objects.filter(
            id_habito=habito,
            fecha_creacion__year=fecha_actual.year,
            fecha_creacion__month=fecha_actual.month
        ).count()

        # Calcular el porcentaje de progreso
        if total_esperado > 0:
            porcentaje = (registros_completados / total_esperado) * 100
            porcentaje = min(porcentaje, 100)  # Asegurar que no exceda 100%
        else:
            porcentaje = 0

        # Datos para la gráfica circular
        data_circular = {
            'completado': registros_completados,
            'restante': max(total_esperado - registros_completados, 0)
        }

        contexto = {
            'titulo': 'Progreso del habito',
            'habito': habito,
            'objetivo': habito.id_objetivo.tipo,
            'categoria': habito.id_categoria,
            'porcentaje': porcentaje,
            'data_circular': data_circular,
            'racha_actual': racha_actual,
            'racha_maxima': racha_maxima
        }

        return render(request, 'mainapp/progreso_habito.html', contexto)
    
def obtener_racha_mas_larga(habito):
    # Obtener los registros del hábito ordenados por fecha de creación
    registros = Registro.objects.filter(id_habito=habito).order_by('fecha_creacion')

    if not registros:
        return 0  # Si no hay registros, la racha es 0

    # Inicializar variables
    racha_actual = 1
    racha_maxima = 1

    # Iterar sobre los registros para comparar fechas
    for i in range(1, len(registros)):
        # Diferencia entre la fecha actual y la anterior
        diferencia_dias = (registros[i].fecha_creacion - registros[i - 1].fecha_creacion).days

        # Si la diferencia es exactamente 1 día, la racha continúa
        if diferencia_dias == 1:
            racha_actual += 1
        else:
            # Si hay una brecha, la racha se reinicia
            racha_maxima = max(racha_maxima, racha_actual)
            racha_actual = 1

    # Al final, actualizar la racha máxima por si la última racha fue la más larga
    racha_maxima = max(racha_maxima, racha_actual)

    return racha_maxima

def obtener_rachas(habito):
    # Obtener los registros del hábito ordenados por fecha de creación
    registros = Registro.objects.filter(id_habito=habito).order_by('fecha_creacion')

    if not registros:
        return 0, 0  # Si no hay registros, las rachas son 0

    # Inicializar variables
    racha_actual = 1
    racha_maxima = 1

    # Inicializamos la racha actual
    for i in range(len(registros)-1, 0, -1):  # Empezamos desde el registro más reciente
        diferencia_dias = (registros[i].fecha_creacion - registros[i - 1].fecha_creacion).days

        # Si la diferencia es exactamente 1 día, la racha actual continúa
        if diferencia_dias == 1:
            racha_actual += 1
        else:
            # Si hay una brecha, detenemos la racha actual
            break

    # Recorremos los registros para encontrar la racha máxima
    racha_temporal = 1
    for i in range(1, len(registros)):
        diferencia_dias = (registros[i].fecha_creacion - registros[i - 1].fecha_creacion).days

        # Si la diferencia es exactamente 1 día, la racha continúa
        if diferencia_dias == 1:
            racha_temporal += 1
        else:
            # Si hay una brecha, comparamos y reiniciamos
            racha_maxima = max(racha_maxima, racha_temporal)
            racha_temporal = 1

    # Al final, actualizar la racha máxima si la última es la más larga
    racha_maxima = max(racha_maxima, racha_temporal)

    return racha_actual, racha_maxima

def editar_recordatorio(request, id_notificacion):
    # Obtiene la notificación por el id proporcionado
    notificacion = get_object_or_404(Notificacion, id_notificacion=id_notificacion)
    
    if request.method == 'POST':
        # Si el método es POST, procesa los datos enviados en el formulario
        form = NotificacionForm(request.POST, instance=notificacion)
        if form.is_valid():
            form.save()
            return redirect('diario')  # Cambia 'nombre_de_la_vista' por la vista a la que redirigirás tras la edición
    else:
        # Si el método es GET, muestra el formulario con los datos actuales
        form = NotificacionForm(instance=notificacion)
    
    # Renderiza la plantilla 'editar_recordatorio.html' con el formulario
    return render(request, 'mainapp/editar_recordatorio.html', {'form': form})