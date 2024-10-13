from datetime import date
from django.utils import timezone
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

def index(request):

    return render(request, 'mainapp/index.html', {
        'titulo': 'Pagina de Inicio'
    })

def diario(request):

    # Obtenemos el usuario que inicio sesion
    usuario_contexto = get_usuario(request)
    usuario = usuario_contexto.get('usuario')

    if usuario is None:
        # Si no hay un usuario en la sesión, redirigir al inicio de sesión
        messages.error(request, 'Debes iniciar sesión para crear un hábito.')
        return redirect('login')

    # Obtenemos los hábitos del usuario que se deben cumplir hoy
    habitos_hoy = obtener_habitos_hoy(usuario)

    # Obtenemos los registros del día de hoy en una sola consulta
    hoy = date.today()
    registros_hoy = Registro.objects.filter(id_habito__in=habitos_hoy, fecha_creacion__date=hoy)

    habitos = []
    for habito in habitos_hoy:
        # Verificamos si el hábito tiene un registro creado hoy
        completado_hoy = registros_hoy.filter(id_habito=habito).exists()

        habitos.append({
            'id_habito': habito.id_habito,
            'objetivo': habito.id_objetivo,  # Ya es un objeto, no hace falta otra consulta
            'categoria': habito.id_categoria,  # Ya es un objeto, no hace falta otra consulta
            'nombre': habito.nombre,
            'frecuencia': habito.frecuencia,
            'completado': completado_hoy  # True si el hábito está completado hoy
        })

    contexto = {
        'titulo': 'Mantente al día',
        'habitos': habitos
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
    categorias = Categoria.objects.all()  # Obtén todas las categorías para el formulario

    if request.method == 'POST':
        habito.nombre = request.POST['nombre']
        habito.descripcion = request.POST.get('descripcion', '')
        habito.frecuencia = request.POST['frecuencia']
        habito.id_categoria_id = request.POST['categoria']
        habito.notificar = 'notificar' in request.POST
        habito.save()  # Guarda los cambios en la base de datos

        return redirect('lista_habitos')  # Redirige a la lista de hábitos después de editar

    return render(request, 'mainapp/editar_habito.html', {
        'habito': habito,
        'categorias': categorias,
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
    # Obtener el hábito correspondiente
    habito = Habito.objects.get(id_habito=id_habito)

    # Crear un nuevo registro relacionado con el hábito y la fecha actual (si no existe ya uno)
    if habito:
        # Verificamos si ya existe un registro relacionado al dia de hoy
        registro = Registro.objects.filter(
            id_habito=habito,
            fecha_creacion__date=timezone.now().date()  # Solo la parte de la fecha
        ).first()
        if registro:
            return HttpResponse('Ya existe un registro')
        else:
            Registro.objects.create(
                id_habito=habito
            )
            return redirect('diario')
    else:
        return HttpResponse('No existe el habito')    


def descompletar_habito(request, id_habito):
    # Obtener el hábito correspondiente
    habito = Habito.objects.get(id_habito=id_habito)

    if habito:
        # Eliminar el registro del día actual relacionado con el hábito
        registro = Registro.objects.filter(
            id_habito=habito,
            fecha_creacion__date=timezone.now().date()  # Solo la parte de la fecha
        ).first()

        if registro:
            registro.delete()
            return redirect('diario')
        else:
            return HttpResponse('No existe el registro')
    else:
        return HttpResponse('No existe el habito')

# Esta clase define un formulario de creación de usuario personalizado, extendiendo el formulario por defecto de Django.
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

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

    
    
    
