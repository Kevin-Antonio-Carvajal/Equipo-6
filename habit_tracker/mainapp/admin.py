from django.contrib import admin
from .models import Categoria, Usuario, Habito, Objetivo, Dia, Registro, Notificacion

# Configuracion para mostrar los modelos en el panel de administracion
class CategoriaAdmin(admin.ModelAdmin):
    readonly_fields = (
        'id_categoria',
    )

# Configuracion para mostrar los modelos en el panel de administracion
class UsuarioAdmin(admin.ModelAdmin):
    readonly_fields = (
        'id_usuario',
    )
    # Evitamos que se muestre la contraseña en el panel de administracion
    exclude = ('password',)

# Configuracion para mostrar los modelos en el panel de administracion
class HabitoAdmin(admin.ModelAdmin):
    readonly_fields = (
        'id_habito',
        'fecha_creacion'
    )

# Configuracion para mostrar los modelos en el panel de administracion
class RegistroAdmin(admin.ModelAdmin):
    readonly_fields = (
        'id_registro',
        'id_habito',
        'fecha_creacion'
    )

# Configuracion para mostrar los modelos en el panel de administracion
class NotificacionAdmin(admin.ModelAdmin):
    readonly_fields = (
        'id_notificacion',
        'id_habito'
    )
    list_display = ('id_notificacion', 'id_habito', 'titulo', 'estatus')
    list_filter = ('estatus',)
    search_fields = ('titulo', 'descripcion')

# Agregamos al panel de administracion
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Habito, HabitoAdmin)
admin.site.register(Registro, RegistroAdmin)
admin.site.register(Objetivo)
admin.site.register(Dia)
admin.site.register(Notificacion, NotificacionAdmin)


