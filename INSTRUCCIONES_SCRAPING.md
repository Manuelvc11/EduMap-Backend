# 🚀 Sistema de Web Scraping de Noticias - Instrucciones Completas

## 📋 Resumen del Sistema

He creado un sistema completo de web scraping de noticias para tu aplicación EduMap. El sistema incluye:

- ✅ **Modelo de datos** para almacenar noticias
- ✅ **API REST** con endpoints fáciles de usar
- ✅ **Scrapers específicos** para sitios populares (BBC, CNN, El País, Marca)
- ✅ **Scraper genérico** para cualquier sitio web
- ✅ **Sistema de configuración** flexible
- ✅ **Comandos de Django** para scraping desde terminal
- ✅ **Tests completos** para validar funcionalidad
- ✅ **Documentación detallada** con ejemplos

## 🛠️ Instalación y Configuración

### 1. Instalar Dependencias

```bash
# Instalar las dependencias de scraping
pip install -r requirements/scraping.txt

# O instalar individualmente:
pip install requests beautifulsoup4 lxml djangorestframework
```

### 2. Configurar la Base de Datos

```bash
# Crear las migraciones (ya creadas manualmente)
python manage.py migrate

# O si prefieres recrearlas:
python manage.py makemigrations noticias
python manage.py migrate
```

### 3. Verificar la Instalación

```bash
# Verificar que la app esté en INSTALLED_APPS
python manage.py check

# Ejecutar el servidor
python manage.py runserver
```

## 🎯 Uso del Sistema

### API Endpoints Disponibles

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/noticias/` | GET | Listar todas las noticias (con paginación) |
| `/api/noticias/scrapear/` | POST | Realizar scraping de un sitio |
| `/api/noticias/{id}/` | GET | Obtener detalles de una noticia |
| `/api/noticias/fuentes/` | GET | Listar fuentes disponibles |

### Ejemplos de Uso

#### 1. Scrapear noticias de BBC
```bash
curl -X POST http://localhost:8000/api/noticias/scrapear/ \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.bbc.com/news", "fuente": "BBC News"}'
```

#### 2. Listar noticias con paginación
```bash
curl "http://localhost:8000/api/noticias/?page=1&per_page=5"
```

#### 3. Obtener fuentes disponibles
```bash
curl "http://localhost:8000/api/noticias/fuentes/"
```

### Comandos de Django

#### Scrapear un sitio específico
```bash
python manage.py scrapear_noticias --sitio bbc --verbose
```

#### Scrapear todos los sitios predefinidos
```bash
python manage.py scrapear_noticias --todos --verbose
```

#### Scrapear una URL personalizada
```bash
python manage.py scrapear_noticias --url "https://elpais.com/" --fuente "El País" --verbose
```

## 📁 Estructura de Archivos Creados

```
applications/noticias/
├── __init__.py
├── admin.py                 # Configuración del admin de Django
├── apps.py                  # Configuración de la aplicación
├── config.py               # Configuración de sitios web
├── logging_config.py       # Configuración de logging
├── models.py               # Modelo de datos Noticia
├── serializers.py          # Serializadores para la API
├── views.py                # Vistas de la API
├── urls.py                 # URLs de la aplicación
├── scrapers.py             # Lógica de web scraping
├── tests.py                # Tests unitarios
├── README.md               # Documentación de la app
├── migrations/             # Migraciones de la BD
│   ├── __init__.py
│   └── 0001_initial.py
└── management/             # Comandos de Django
    └── commands/
        └── scrapear_noticias.py
```

## 🔧 Personalización

### Agregar un Nuevo Sitio Web

1. **Editar `scrapers.py`** y agregar un nuevo método:
```python
def _scrapear_nuevo_sitio(self, soup, base_url):
    noticias = []
    # Tu lógica de scraping aquí
    return noticias
```

2. **Actualizar `_determinar_scraper`**:
```python
elif 'nuevo-sitio.com' in domain:
    return self._scrapear_nuevo_sitio(soup, url)
```

3. **Agregar configuración en `config.py`**:
```python
SITIOS_NOTICIAS['nuevo_sitio'] = {
    'nombre': 'Nuevo Sitio',
    'urls': ['https://nuevo-sitio.com/'],
    'selectores': {
        'articulos': 'article',
        'titulo': 'h2',
        'enlace': 'a',
        'resumen': 'p',
        'imagen': 'img'
    }
}
```

### Modificar Configuración

Edita `config.py` para cambiar:
- Timeouts de conexión
- Número máximo de noticias
- Palabras clave de filtrado
- Selectores CSS

## 🧪 Testing

### Ejecutar Tests
```bash
python manage.py test applications.noticias
```

### Tests Incluidos
- ✅ Tests del modelo Noticia
- ✅ Tests de la API REST
- ✅ Tests del ScrapingManager
- ✅ Tests de manejo de errores

## 📊 Monitoreo y Logging

### Ver Logs
```bash
# Los logs se guardan en logs/scraping.log
tail -f logs/scraping.log
```

### Configurar Logging
Edita `logging_config.py` para personalizar:
- Nivel de logging
- Formato de mensajes
- Archivos de log
- Rotación de logs

## 🚨 Consideraciones Importantes

### Ética y Legalidad
1. **Respeta los robots.txt** de cada sitio
2. **No hagas demasiadas peticiones** seguidas
3. **Cumple con los términos de servicio** de cada sitio
4. **No extraigas información personal**

### Rendimiento
1. **Usa delays** entre peticiones
2. **Implementa rate limiting** si es necesario
3. **Limpia noticias antiguas** regularmente
4. **Monitorea el uso de memoria**

### Mantenimiento
1. **Actualiza los selectores** si los sitios cambian
2. **Revisa los logs** regularmente
3. **Ejecuta tests** antes de desplegar
4. **Haz backup** de la base de datos

## 🎉 ¡Listo para Usar!

El sistema está completamente configurado y listo para usar. Puedes:

1. **Empezar a scrapear** noticias inmediatamente
2. **Personalizar** los sitios web según tus necesidades
3. **Integrar** la API en tu frontend
4. **Extender** el sistema con nuevas funcionalidades

### Próximos Pasos Sugeridos

1. **Probar el sistema** con los ejemplos proporcionados
2. **Personalizar** los sitios web según tus intereses
3. **Integrar** la API en tu aplicación frontend
4. **Configurar** un cron job para scraping automático
5. **Implementar** notificaciones de nuevas noticias

¡El sistema está diseñado para ser fácil de usar y extender, perfecto para principiantes! 🚀
