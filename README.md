# Proyecto Intermedio Equipo 6

**Repositorio**: https://github.com/Kevin-Antonio-Carvajal/Equipo-6

# Aplicación de Seguimiento de Hábitos
Repositorio oficial del Proyecto Intermedio "Aplicación de Seguimiento de Hábitos" para la materia de **Diseño de Interfaces de Usuario** de la **Facultad de Ciencias de la UNAM** en el semestre 2025-1.

## Profesores:

- Dario Emmanuel Vázquez Ceballos
- Alejandro Gónzalez Ruíz
- Andrea Uxue Amaya Navarrete
- María Fernanda Mendoza Castillo

## Alumnos:
- Arrieta Mancera Luis Sebastian
- Antonio Carvajal Kevin
- Morales Hidalgo Pedro
- Mendiola Montes Victor Manuel
- García Zárraga Angélica Lizbeth
- Rodríguez García Ulises

# Ejecución:

1. **Creación y activación del entorno virtual**:
   
   Para ejecutar este proyecto, es necesario crear y activar un entorno virtual. Los pasos para hacerlo son los siguientes:

   #### En macOS/Linux:
   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

   #### En Windows:
   ```bash
   python3 -m venv env
   .\env\Scripts\activate
   ```

2. **Instalación de dependencias**:
   
   Con el entorno virtual activado, instala todas las dependencias necesarias ejecutando el siguiente comando:

   ```bash
   pip3 install -r requirements.txt
   ```

3. **Ejecución del servidor de desarrollo**:
   
   Con las dependencias instaladas y el entorno virtual activo, puedes iniciar el servidor de desarrollo con el siguiente comando:

   ```bash
   python3 manage.py runserver
   ```

# Desarrollo

## `/mainapp`

Aplicacion principal, aqui se agregan las cosas en general como el inicio de sesion y la pagina principal.

# Administradores

Comando para crear super usuarios:

```bash
python3 manage.py createsuperuser
```

Ejemplo:

**Usuario:** sebs

**Correo:** sebastian_luis@ciencias.unam.mx

# Ayuda
En caso de que los estilos CSS no se vean reflejados en la página, presiona `Ctrl+F5`, esto sucede porque el navegador guarda los estilos css en caché.

