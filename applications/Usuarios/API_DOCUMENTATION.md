# API de Inicio de Sesión - EduMap

Esta aplicación proporciona endpoints de API para el manejo de autenticación y perfiles de usuario.

## Endpoints Disponibles

### 1. Registro de Usuario
**POST** `/register/`

Registra un nuevo usuario en el sistema.

**Body (JSON):**
```json
{
    "username": "usuario123",
    "email": "usuario@ejemplo.com",
    "password1": "contraseña123",
    "password2": "contraseña123",
    "first_name": "Juan",
    "last_name": "Pérez"
}
```

**Respuesta exitosa (201):**
```json
{
    "success": true,
    "message": "¡Cuenta creada exitosamente! Ahora puedes iniciar sesión.",
    "user": {
        "id": 1,
        "username": "usuario123",
        "email": "usuario@ejemplo.com",
        "first_name": "Juan",
        "last_name": "Pérez"
    }
}
```

### 2. Inicio de Sesión
**POST** `/login/`

Autentica un usuario existente.

**Body (JSON):**
```json
{
    "username": "usuario123",
    "password": "contraseña123"
}
```

**Respuesta exitosa (200):**
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
        "date_joined": "2024-01-01T10:00:00Z"
    }
}
```

### 3. Cerrar Sesión
**POST** `/logout/`

Cierra la sesión del usuario autenticado.

**Respuesta exitosa (200):**
```json
{
    "success": true,
    "message": "Has cerrado sesión correctamente"
}
```

### 4. Dashboard
**GET** `/dashboard/`

Obtiene información del usuario autenticado y su perfil.

**Headers requeridos:**
- Autenticación de sesión (usuario debe estar logueado)

**Respuesta exitosa (200):**
```json
{
    "success": true,
    "user": {
        "id": 1,
        "username": "usuario123",
        "email": "usuario@ejemplo.com",
        "first_name": "Juan",
        "last_name": "Pérez",
        "is_active": true,
        "date_joined": "2024-01-01T10:00:00Z"
    },
    "perfil": {
        "telefono": "+1234567890",
        "fecha_nacimiento": "1990-01-01",
        "direccion": "Calle 123, Ciudad",
        "avatar": "/media/avatars/avatar.jpg",
        "fecha_creacion": "2024-01-01T10:00:00Z",
        "fecha_actualizacion": "2024-01-01T10:00:00Z"
    }
}
```

### 5. Obtener Perfil
**GET** `/profile/`

Obtiene la información del perfil del usuario autenticado.

**Headers requeridos:**
- Autenticación de sesión

**Respuesta exitosa (200):**
```json
{
    "success": true,
    "perfil": {
        "telefono": "+1234567890",
        "fecha_nacimiento": "1990-01-01",
        "direccion": "Calle 123, Ciudad",
        "avatar": "/media/avatars/avatar.jpg",
        "fecha_creacion": "2024-01-01T10:00:00Z",
        "fecha_actualizacion": "2024-01-01T10:00:00Z"
    }
}
```

### 6. Actualizar Perfil
**POST** `/profile/`

Actualiza la información del perfil del usuario autenticado.

**Headers requeridos:**
- Autenticación de sesión

**Body (JSON):**
```json
{
    "telefono": "+0987654321",
    "fecha_nacimiento": "1990-01-01",
    "direccion": "Nueva dirección 456"
}
```

**Respuesta exitosa (200):**
```json
{
    "success": true,
    "message": "Perfil actualizado correctamente",
    "perfil": {
        "telefono": "+0987654321",
        "fecha_nacimiento": "1990-01-01",
        "direccion": "Nueva dirección 456",
        "avatar": "/media/avatars/avatar.jpg",
        "fecha_creacion": "2024-01-01T10:00:00Z",
        "fecha_actualizacion": "2024-01-01T11:00:00Z"
    }
}
```

## Códigos de Estado HTTP

- **200**: Éxito
- **201**: Creado exitosamente
- **400**: Error en la solicitud (datos inválidos)
- **401**: No autorizado (credenciales inválidas)
- **405**: Método no permitido
- **500**: Error interno del servidor

## Ejemplos de Uso con cURL

### Registro
```bash
curl -X POST http://localhost:8000/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@ejemplo.com",
    "password1": "testpass123",
    "password2": "testpass123",
    "first_name": "Test",
    "last_name": "User"
  }'
```

### Inicio de Sesión
```bash
curl -X POST http://localhost:8000/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'
```

### Dashboard (con cookies de sesión)
```bash
curl -X GET http://localhost:8000/dashboard/ \
  -H "Cookie: sessionid=tu_session_id_aqui"
```

## Notas Importantes

1. **Autenticación**: La aplicación usa el sistema de sesiones de Django. Después del login, las cookies de sesión deben incluirse en las solicitudes subsiguientes.

2. **CSRF**: Los endpoints están exentos de CSRF para facilitar el uso como API, pero en producción se recomienda implementar autenticación por tokens.

3. **Archivos**: El campo `avatar` en el perfil maneja archivos de imagen. Para subir archivos, se debe usar `multipart/form-data` en lugar de JSON.

4. **Fechas**: Todas las fechas se devuelven en formato ISO 8601 (YYYY-MM-DDTHH:MM:SSZ).
