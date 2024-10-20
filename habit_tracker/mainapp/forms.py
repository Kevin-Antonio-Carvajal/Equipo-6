from django import forms
from django.core import validators
from .models import Notificacion

class FormRegister(forms.Form):

    nombre = forms.CharField(
        label="Nombre completo",
        max_length=255,
        min_length=2,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': '',
            'class': 'campo-nombre',  # Clase CSS (por ejemplo, para Bootstrap)
        })
    )

    username = forms.CharField(
        label="Nombre de usuario",
        max_length=64,
        min_length=3,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': '',
            'class': 'campo-username'
        })
    )

    correo = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                'placeholder': ''
            }
        )
    )    

    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(
            attrs={
                'required': True,
                'autocomplete': 'off'
            }
        ),        
    )

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