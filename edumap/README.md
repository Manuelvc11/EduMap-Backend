# EduMap Backend

Backend del proyecto EduMap desarrollado con Django.

## Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git

## Instalación y Configuración

### 1. Clonar el Repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd EduMap-Backend
```

### 2. Crear y Activar el Entorno Virtual

#### En Windows (PowerShell):
```powershell
# Crear el entorno virtual
python -m venv venv

# Activar el entorno virtual
.\venv\Scripts\Activate.ps1
```

#### En Windows (Command Prompt):
```cmd
# Crear el entorno virtual
python -m venv venv

# Activar el entorno virtual
venv\Scripts\activate.bat
```

#### En macOS/Linux:
```bash
# Crear el entorno virtual
python3 -m venv venv

# Activar el entorno virtual
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
# Asegúrate de que el entorno virtual esté activado
pip install -r requirements.txt
```

**Nota:** Si no existe el archivo `requirements.txt`, instala Django manualmente:
```bash
pip install django
```

### 4. Configurar la Base de Datos

```bash
# Navegar al directorio del proyecto Django
cd edumap

# Ejecutar las migraciones
python manage.py migrate

# Crear un superusuario (opcional)
python manage.py createsuperuser
```

### 5. Ejecutar el Servidor de Desarrollo

```bash
# Asegúrate de estar en el directorio edumap/
python manage.py runserver
```

El servidor estará disponible en: http://127.0.0.1:8000/

## Estructura del Proyecto

```
EduMap-Backend/
├── edumap/                 # Proyecto Django principal
│   ├── edumap/            # Configuración del proyecto
│   │   ├── __init__.py
│   │   ├── settings.py    # Configuraciones de Django
│   │   ├── urls.py        # URLs principales
│   │   ├── wsgi.py        # Configuración WSGI
│   │   └── asgi.py        # Configuración ASGI
│   ├── manage.py          # Script de administración de Django
│   └── db.sqlite3         # Base de datos SQLite
├── README.md               # Este archivo
└── .gitignore             # Archivos a ignorar por Git
```

## Comandos Útiles

```bash
# Crear una nueva aplicación Django
python manage.py startapp nombre_app

# Hacer migraciones después de cambios en modelos
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Ejecutar tests
python manage.py test

# Abrir shell de Django
python manage.py shell

# Recolectar archivos estáticos
python manage.py collectstatic
```

## Desactivar el Entorno Virtual

Cuando termines de trabajar en el proyecto:

```bash
deactivate
```

## Contribución

1. Asegúrate de que el entorno virtual esté activado antes de trabajar
2. Instala las nuevas dependencias si las agregas
3. Actualiza el archivo `requirements.txt` si es necesario:
   ```bash
   pip freeze > requirements.txt
   ```

## Solución de Problemas

### Error de permisos en PowerShell
Si tienes problemas con la política de ejecución en PowerShell, ejecuta:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Puerto ya en uso
Si el puerto 8000 está ocupado, puedes especificar otro:
```bash
python manage.py runserver 8001
```

## Licencia

[Especificar la licencia del proyecto]
