# API Documentation - Progreso Usuario

## Descripción
La aplicación `progreso_usuario` permite gestionar y rastrear el progreso de los usuarios en diferentes actividades o tareas. Incluye funcionalidades para crear, editar, visualizar y eliminar registros de progreso, así como un sistema de logs para mantener un historial de cambios.

## Modelos

### ProgresoUsuario
Modelo principal que almacena el progreso de los usuarios.

**Campos:**
- `usuario` (ForeignKey): Usuario asociado al progreso
- `actividad` (CharField): Nombre de la actividad (máximo 100 caracteres)
- `progreso` (DecimalField): Porcentaje de progreso (0.00 - 100.00)
- `fecha_inicio` (DateTimeField): Fecha de creación (automática)
- `fecha_actualizacion` (DateTimeField): Última actualización (automática)
- `completado` (BooleanField): Indica si la actividad está completada
- `notas` (TextField): Notas adicionales (opcional)

**Restricciones:**
- Combinación única de usuario y actividad
- Progreso entre 0.00 y 100.00

### LogProgreso
Modelo para registrar el historial de cambios en el progreso.

**Campos:**
- `progreso_usuario` (ForeignKey): Referencia al progreso
- `progreso_anterior` (DecimalField): Valor anterior del progreso
- `progreso_nuevo` (DecimalField): Nuevo valor del progreso
- `fecha_cambio` (DateTimeField): Fecha del cambio (automática)
- `descripcion` (TextField): Descripción del cambio (opcional)

## URLs

| URL | Nombre | Descripción |
|-----|--------|-------------|
| `/progreso/` | `lista` | Lista todos los progresos del usuario |
| `/progreso/crear/` | `crear` | Formulario para crear nuevo progreso |
| `/progreso/<id>/` | `detalle` | Detalle de un progreso específico |
| `/progreso/<id>/editar/` | `editar` | Formulario para editar progreso |
| `/progreso/<id>/eliminar/` | `eliminar` | Confirmación para eliminar progreso |
| `/progreso/<id>/actualizar-ajax/` | `actualizar_ajax` | Actualización AJAX del progreso |

## Vistas

### lista_progreso
- **Método:** GET
- **Autenticación:** Requerida
- **Funcionalidad:** Lista el progreso del usuario con filtros y paginación
- **Filtros disponibles:**
  - `actividad`: Buscar por nombre de actividad
  - `completado`: Filtrar por estado de completado

### detalle_progreso
- **Método:** GET
- **Autenticación:** Requerida
- **Funcionalidad:** Muestra el detalle de un progreso específico y su historial de logs

### crear_progreso
- **Método:** GET, POST
- **Autenticación:** Requerida
- **Funcionalidad:** Crea un nuevo registro de progreso

### editar_progreso
- **Método:** GET, POST
- **Autenticación:** Requerida
- **Funcionalidad:** Edita un progreso existente y crea log automático

### actualizar_progreso_ajax
- **Método:** POST
- **Autenticación:** Requerida
- **Funcionalidad:** Actualización rápida del progreso vía AJAX
- **Respuesta JSON:**
  ```json
  {
    "success": true,
    "progreso": 75.00,
    "completado": false
  }
  ```

### eliminar_progreso
- **Método:** GET, POST
- **Autenticación:** Requerida
- **Funcionalidad:** Elimina un registro de progreso

## Formularios

### ProgresoUsuarioForm
Formulario para crear y editar progreso de usuario.

**Campos:**
- `actividad`: Campo de texto para el nombre de la actividad
- `progreso`: Campo numérico (0-100) para el porcentaje
- `completado`: Checkbox para marcar como completado
- `notas`: Área de texto para notas adicionales

**Validaciones:**
- Progreso entre 0 y 100
- Si está completado, el progreso se ajusta automáticamente a 100%

### FiltroProgresoForm
Formulario para filtrar la lista de progresos.

**Campos:**
- `actividad`: Búsqueda por nombre de actividad
- `completado`: Filtro por estado (Todos/Completados/En progreso)

## Admin

### ProgresoUsuarioAdmin
Configuración del admin para el modelo ProgresoUsuario.

**Características:**
- Lista con campos principales
- Filtros por completado, actividad y fechas
- Búsqueda por usuario y actividad
- Edición en línea de progreso y estado completado
- Fieldsets organizados

### LogProgresoAdmin
Configuración del admin para el modelo LogProgreso.

**Características:**
- Solo lectura (no se pueden crear logs manualmente)
- Filtros por fecha y actividad
- Búsqueda por usuario y descripción

## Tests

La aplicación incluye tests completos que cubren:

1. **Modelos:**
   - Creación de progreso de usuario
   - Validación de restricciones únicas
   - Marcado como completado

2. **Vistas:**
   - Requerimiento de autenticación
   - Lista de progresos
   - Detalle de progreso
   - Creación de nuevo progreso
   - Actualización AJAX

3. **Logs:**
   - Creación de logs de progreso

## Instalación

1. Agregar la aplicación a `INSTALLED_APPS` en settings.py:
   ```python
   INSTALLED_APPS = [
       # ... otras aplicaciones
       'applications.progreso_usuario',
   ]
   ```

2. Incluir las URLs en el archivo principal de URLs:
   ```python
   urlpatterns = [
       # ... otras URLs
       path('progreso/', include('applications.progreso_usuario.urls')),
   ]
   ```

3. Ejecutar migraciones:
   ```bash
   python manage.py makemigrations progreso_usuario
   python manage.py migrate
   ```

## Uso

1. **Crear progreso:** Los usuarios pueden crear nuevos registros de progreso para diferentes actividades
2. **Actualizar progreso:** Se puede actualizar el porcentaje de progreso y marcar como completado
3. **Ver historial:** Cada cambio se registra automáticamente en el log
4. **Filtrar y buscar:** La lista permite filtrar por actividad y estado de completado
5. **Eliminar:** Los usuarios pueden eliminar registros de progreso que ya no necesiten

## Características Adicionales

- **Paginación:** La lista de progresos incluye paginación (10 elementos por página)
- **Logs automáticos:** Cada cambio en el progreso genera un log automático
- **Validaciones:** Formularios con validaciones para asegurar datos consistentes
- **Interfaz responsive:** Formularios con clases CSS para Bootstrap
- **Seguridad:** Solo los usuarios pueden ver y editar sus propios progresos
