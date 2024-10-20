from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
import re
from .models import Notificacion

class FormRegister(forms.Form):

    nombre = forms.CharField(
        label="Nombre completo",
        max_length=255,
        min_length=2,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    username = forms.CharField(
        label="Nombre de usuario",
        max_length=64,
        min_length=3,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    correo = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )    

    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True    
    )

    # Validación personalizada del nombre
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if len(nombre) > 30:
            raise ValidationError('El nombre no debe tener más de 30 caracteres.')
        if nombre.isdigit():
            raise ValidationError('El nombre completo no puede contener solo números.')
        return nombre

    # Validación personalizada del nombre de usuario
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) > 30:
            raise ValidationError('El nombre de usuario no debe tener más de 30 caracteres.')
        if username.isdigit():
            raise ValidationError('El nombre de usuario no puede contener solo números.')
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise ValidationError('El nombre de usuario solo puede contener letras, números y guiones bajos.')
        return username

    # Validación personalizada de la contraseña
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not re.search(r'[A-Z]', password):
            raise ValidationError('La contraseña debe tener al menos una letra mayúscula.')
        if not re.search(r'[a-z]', password):
            raise ValidationError('La contraseña debe tener al menos una letra minúscula.')
        if not re.search(r'\d', password):
            raise ValidationError('La contraseña debe tener al menos un número.')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError('La contraseña debe tener al menos un carácter especial.')
        return password

class FormLogin(forms.Form):
    
    correo = forms.EmailField(
        required=True,
    )    

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'required': True,
                'autocomplete': 'off'
            }
        ),
        required=True,
    )

class NotificacionForm(forms.ModelForm):
    class Meta:
        model = Notificacion
        fields = ['titulo', 'descripcion', 'mensaje_motivacional']