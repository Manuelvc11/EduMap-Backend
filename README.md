# EduMap Backend

Backend del proyecto EduMap desarrollado con Django. API REST para la gestión de usuarios y progreso de actividades educativas.

## Documentación de la API

### Endpoints de Usuarios

#### Registro de Usuario
```http
POST /api/usuarios/register/
```
Request Body:
```json
{
    "email": "usuario@ejemplo.com",
    "password": "contraseña123",
    "username": "usuario123",
    "first_name": "Juan",
    "last_name": "Pérez"
}
```

#### Inicio de Sesión
```http
POST /api/usuarios/login/
```
Request Body:
```json
{
    "username": "usuario123",
    "password": "contraseña123"
}
```

#### Dashboard de Usuario
```http
GET /api/usuarios/dashboard/
```
Headers requeridos:
- Cookie: sessionid=<your_session_id>

#### Perfil de Usuario
```http
GET /api/usuarios/profile/
POST /api/usuarios/profile/
```
Para actualizar el perfil (POST):
```json
{
    "telefono": "1234567890",
    "fecha_nacimiento": "1990-01-01",
    "direccion": "Calle Principal 123"
}
```

### Endpoints de Progreso

#### Listar Progresos
```http
GET /api/progreso/
```

#### Crear Progreso
```http
POST /api/progreso/crear/
```
Request Body:
```json
{
    "actividad": "Matemáticas",
    "progreso": 75
}
```

#### Actualizar Progreso
```http
POST /api/progreso/{id}/actualizar/
```
Request Body:
```json
{
    "progreso": 85
}
```

#### Detalle de Progreso
```http
GET /api/progreso/{id}/
```

#### Eliminar Progreso
```http
POST /api/progreso/{id}/eliminar/
```

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

## Respuestas de la API

### Respuestas de Usuario

#### Registro Exitoso
```json
{
    "success": true,
    "message": "¡Cuenta creada exitosamente! Ahora puedes iniciar sesión.",
    "user": {
        "id": 1,
        "email": "usuario@ejemplo.com",
        "username": "usuario123",
        "first_name": "Juan",
        "last_name": "Pérez",
        "nombre_completo": "Juan Pérez"
    }
}
```

#### Inicio de Sesión Exitoso
```json
{
    "success": true,
    "message": "¡Bienvenido, Juan!",
    "user": {
        "id": 1,
        "username": "usuario123",
        "email": "usuario@ejemplo.com",
        "first_name": "Juan",
        "last_name": "Pérez",
        "is_active": true,
        "date_joined": "2025-10-14T12:00:00Z"
    }
}
```

#### Dashboard
```json
{
    "success": true,
    "user": {
        "id": 1,
        "username": "usuario123",
        "email": "usuario@ejemplo.com",
        "first_name": "Juan",
        "last_name": "Pérez",
        "nombre_completo": "Juan Pérez",
        "is_active": true,
        "date_joined": "2025-10-14T12:00:00Z"
    },
    "perfil": {
        "telefono": "1234567890",
        "fecha_nacimiento": "1990-01-01",
        "direccion": "Calle Principal 123",
        "avatar": "/media/avatars/usuario123.jpg",
        "fecha_creacion": "2025-10-14T12:00:00Z",
        "fecha_actualizacion": "2025-10-14T12:00:00Z"
    }
}
```

### Respuestas de Progreso

#### Actualización de Progreso
```json
{
    "success": true,
    "data": {
        "id": 5,
        "progreso": 85.0,
        "completado": false,
        "fecha_actualizacion": "2025-10-14T12:00:00Z"
    },
    "message": "Progreso actualizado correctamente"
}
```

## Estructura del Proyecto

```
EduMap-Backend/
├── applications/           # Aplicaciones Django
│   ├── Usuarios/          # Aplicación de usuarios
│   └── progreso_usuario/  # Aplicación de progreso de usuarios
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

## Endpoints de la API

### Aplicación: Usuarios

#### Autenticación y Gestión de Usuarios
| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| GET | `/` | Información de la API y endpoints disponibles | ❌ No requerida |
| POST | `/usuarios/login/` | Iniciar sesión | ❌ No requerida |
| POST | `/usuarios/logout/` | Cerrar sesión | ❌ No requerida |
| POST | `/usuarios/register/` | Registrar nuevo usuario | ❌ No requerida |
| GET | `/usuarios/dashboard/` | Dashboard del usuario autenticado | ✅ Requerida |
| GET | `/usuarios/profile/` | Ver perfil del usuario | ✅ Requerida |
| POST | `/usuarios/profile/` | Actualizar perfil del usuario | ✅ Requerida |

#### Parámetros de Request

**POST `/usuarios/login/`:**
```json
{
    "username": "usuario123",
    "password": "contraseña123"
}
```

**POST `/usuarios/register/`:**
```json
{
    "username": "usuario123",
    "email": "usuario@ejemplo.com",
    "password": "contraseña123"
}
```

**POST `/usuarios/profile/`:**
```json
{
    "telefono": "+1234567890",
    "fecha_nacimiento": "1990-01-01",
    "direccion": "Calle Principal 123"
}
```

#### Ejemplos de Respuesta

**Login exitoso:**
```json
{
    "success": true,
    "message": "¡Bienvenido, Usuario!",
    "user": {
        "id": 1,
        "username": "usuario123",
        "email": "usuario@ejemplo.com",
        "first_name": "Usuario",
        "last_name": "Apellido",
        "is_active": true,
        "date_joined": "2024-01-01T10:00:00Z"
    }
}
```

**Dashboard:**
```json
{
    "success": true,
    "user": {
        "id": 1,
        "username": "usuario123",
        "email": "usuario@ejemplo.com",
        "first_name": "Usuario",
        "last_name": "Apellido",
        "is_active": true,
        "date_joined": "2024-01-01T10:00:00Z"
    },
    "perfil": {
        "telefono": "+1234567890",
        "fecha_nacimiento": "1990-01-01",
        "direccion": "Calle Principal 123",
        "avatar": "/media/avatars/avatar.jpg",
        "fecha_creacion": "2024-01-01T10:00:00Z",
        "fecha_actualizacion": "2024-01-15T14:30:00Z"
    }
}
```

### Aplicación: Progreso Usuario

#### Gestión de Progreso
| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| GET | `/progreso/` | Lista todos los progresos del usuario | ✅ Requerida |
| POST | `/progreso/crear/` | Crea un nuevo progreso | ✅ Requerida |
| GET | `/progreso/<id>/` | Detalle de un progreso específico | ✅ Requerida |
| GET | `/progreso/<id>/editar/` | Formulario de edición | ✅ Requerida |
| POST | `/progreso/<id>/editar/` | Actualiza un progreso | ✅ Requerida |
| GET | `/progreso/<id>/eliminar/` | Confirmación de eliminación | ✅ Requerida |
| POST | `/progreso/<id>/eliminar/` | Elimina un progreso | ✅ Requerida |
| POST | `/progreso/<id>/actualizar-ajax/` | Actualización rápida vía AJAX | ✅ Requerida |

#### Parámetros de Filtrado (GET `/progreso/`)
- `actividad`: Filtrar por nombre de actividad
- `completado`: Filtrar por estado (true/false)
- `page`: Número de página para paginación

#### Ejemplo de Respuesta AJAX (POST `/progreso/<id>/actualizar-ajax/`)
```json
{
    "success": true,
    "progreso": 75.00,
    "completado": false
}
```

#### Modelos de Datos

**Usuario (Django Auth):**
```json
{
    "id": 1,
    "username": "usuario123",
    "email": "usuario@ejemplo.com",
    "first_name": "Usuario",
    "last_name": "Apellido",
    "is_active": true,
    "date_joined": "2024-01-01T10:00:00Z"
}
```

**PerfilUsuario:**
```json
{
    "id": 1,
    "usuario": 1,
    "telefono": "+1234567890",
    "fecha_nacimiento": "1990-01-01",
    "direccion": "Calle Principal 123",
    "avatar": "/media/avatars/avatar.jpg",
    "fecha_creacion": "2024-01-01T10:00:00Z",
    "fecha_actualizacion": "2024-01-15T14:30:00Z"
}
```

**ProgresoUsuario:**
```json
{
    "id": 1,
    "usuario": "username",
    "actividad": "Aprender Django",
    "progreso": 75.50,
    "fecha_inicio": "2024-01-01T10:00:00Z",
    "fecha_actualizacion": "2024-01-15T14:30:00Z",
    "completado": false,
    "resultado": "Notas sobre el progreso"
}
```

**LogProgreso:**
```json
{
    "id": 1,
    "progreso_usuario": 1,
    "progreso_anterior": 50.00,
    "progreso_nuevo": 75.50,
    "fecha_cambio": "2024-01-15T14:30:00Z",
    "descripcion": "Progreso actualizado"
}
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
