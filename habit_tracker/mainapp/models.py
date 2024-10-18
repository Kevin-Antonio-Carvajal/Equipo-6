from django.db import models

# TABLA USUARIO
class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)  # AUTO_INCREMENT y PRIMARY KEY
    nombre = models.CharField(max_length=255)  # VARCHAR(255)
    correo = models.EmailField(max_length=255, unique=True)  # VARCHAR(255), UNIQUE
    username = models.CharField(max_length=64, unique=True)  # VARCHAR(64), UNIQUE
    password = models.CharField(max_length=64)  # VARCHAR(64)

    def __str__(self):
        return self.username
    
# TABLA OBJETIVO
class Objetivo(models.Model):
    TIPO_CHOICES = [
        ('diario', 'Diario'),
        ('semanal', 'Semanal'),
        ('mensual', 'Mensual'),
    ]
    
    id_objetivo = models.AutoField(primary_key=True)  # AUTO_INCREMENT y PRIMARY KEY
    tipo = models.CharField(max_length=8, choices=TIPO_CHOICES, default='diario')  # ENUM con valores 'diario', 'semanal', 'mensual'

    def __str__(self):
        return self.tipo

# TABLA DIA
class Dia(models.Model):
    id_objetivo = models.ForeignKey('Objetivo', on_delete=models.CASCADE)  # Clave foránea a Objetivo
    dia = models.PositiveIntegerField()  # INT para representar los días del 1 al 31

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(dia__gte=1, dia__lte=31), name='dia_valid_range')  # CHECK constraint para el rango de días
        ]
        unique_together = ('id_objetivo', 'dia')  # Llave primaria compuesta

    def __str__(self):
        return f"{self.id_objetivo} - Día {self.dia}"

# TABLA HABITO
class Habito(models.Model):
    id_habito = models.AutoField(primary_key=True)  # AUTO_INCREMENT y PRIMARY KEY
    id_usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)  # ForeignKey a Usuario
    id_objetivo = models.ForeignKey('Objetivo', on_delete=models.CASCADE)  # ForeignKey a Objetivo
    id_categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)  # ForeignKey a Categoria
    nombre = models.CharField(max_length=64)  # VARCHAR(64)
    descripcion = models.CharField(max_length=255, null=True, blank=True)  # VARCHAR(255) con DEFAULT NULL
    frecuencia = models.PositiveIntegerField(default=1)  # INT con DEFAULT 1
    titulo_recordatorio = models.CharField(max_length=64, default='No olvides que tienes un objetivo')  # VARCHAR(64) con DEFAULT
    mensaje_recordatorio = models.CharField(max_length=255, default='Recuerda que cada día se vuelve más fácil, lo dificil es hacerlo todos los días.')  # VARCHAR(255) con DEFAULT
    notificar = models.BooleanField(default=True)  # BOOLEAN con DEFAULT TRUE
    estatus = models.BooleanField(default=True)  # BOOLEAN con DEFAULT TRUE
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # TIMESTAMP con DEFAULT current_timestamp()

    def __str__(self):
        return self.nombre

# TABLA CATEGORIA
class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)  # AUTO_INCREMENT y PRIMARY KEY
    nombre = models.CharField(max_length=64)  # VARCHAR(64)
    descripcion = models.TextField(null=True, blank=True)  # TEXT con DEFAULT NULL
    color = models.CharField(max_length=7)  # CHAR(7) para almacenar el color en formato hexadecimal

    def __str__(self):
        return self.nombre
    
# TABLA REGISTRO
class Registro(models.Model):
    id_registro = models.AutoField(primary_key=True)  # AUTO_INCREMENT y PRIMARY KEY
    id_habito = models.ForeignKey('Habito', on_delete=models.CASCADE)  # Clave foránea a Habito
    estatus = models.BooleanField(default=True)  # BOOLEAN con DEFAULT TRUE
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # TIMESTAMP con DEFAULT current_timestamp()

    def __str__(self):
        return f"Registro {self.id_registro} - Hábito {self.id_habito}"
    
# TABLA RECORDATORIO
class Recordatorio(models.Model):
    id_habito = models.ForeignKey('Habito', on_delete=models.CASCADE)  # Clave foránea a Habito
    hora = models.TimeField()  # TIME para la hora del recordatorio

    class Meta:
        unique_together = ('id_habito', 'hora')  # Llave primaria compuesta

    def __str__(self):
        return f"Recordatorio para {self.id_habito} a las {self.hora}"

# TABLA NOTIFICACION
class Notificacion(models.Model):
    id_notificacion = models.AutoField(primary_key=True)  # AUTO_INCREMENT y PRIMARY KEY        
    id_habito = models.ForeignKey('Habito', on_delete=models.CASCADE)  # ForeignKey a Habito
    titulo = models.CharField(max_length=64)  # VARCHAR(64)
    descripcion = models.CharField(max_length=255, null=True, blank=True)  # VARCHAR(255)
    estatus = models.BooleanField(default=False)  # BOOLEAN con DEFAULT FALSE
    mensaje_motivacional = models.CharField(max_length=255, null=True, blank=True)  # Mensaje opcional
    def __str__(self):
        return f"{self.titulo}: {self.mensaje_motivacional or 'Mantente motivado!'}"
