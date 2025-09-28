# Sistema de Web Scraping de Noticias

Este módulo proporciona una solución completa y fácil de usar para realizar web scraping de noticias desde diferentes sitios web.

## Características

- ✅ **Fácil de usar**: Diseñado para principiantes
- ✅ **Múltiples fuentes**: Soporte para BBC, CNN, El País, Marca y sitios genéricos
- ✅ **API REST**: Endpoints fáciles de consumir
- ✅ **Prevención de duplicados**: Evita noticias repetidas
- ✅ **Manejo de errores**: Logging y manejo robusto de errores
- ✅ **Configuración flexible**: Fácil de personalizar

## Instalación

1. Instalar las dependencias:
```bash
pip install -r requirements/scraping.txt
```

2. Agregar la aplicación a `INSTALLED_APPS` en `settings.py` (ya incluido)

3. Ejecutar migraciones:
```bash
python manage.py makemigrations noticias
python manage.py migrate
```

## Uso de la API

### 1. Listar todas las noticias
```http
GET /api/noticias/
```

Parámetros opcionales:
- `page`: Número de página (default: 1)
- `per_page`: Noticias por página (default: 10)

### 2. Realizar scraping de un sitio
```http
POST /api/noticias/scrapear/
Content-Type: application/json

{
    "url": "https://www.bbc.com/news",
    "fuente": "BBC News"
}
```

### 3. Obtener detalles de una noticia
```http
GET /api/noticias/{id}/
```

### 4. Listar fuentes disponibles
```http
GET /api/noticias/fuentes/
```

## Ejemplos de uso con cURL

### Scrapear noticias de BBC
```bash
curl -X POST http://localhost:8000/api/noticias/scrapear/ \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.bbc.com/news", "fuente": "BBC News"}'
```

### Obtener noticias con paginación
```bash
curl "http://localhost:8000/api/noticias/?page=1&per_page=5"
```

## Sitios web soportados

### Sitios específicos (con scrapers optimizados):
- **BBC News**: `https://www.bbc.com/news`
- **CNN**: `https://www.cnn.com/`
- **El País**: `https://elpais.com/`
- **Marca**: `https://www.marca.com/`

### Sitios genéricos:
Cualquier sitio web que contenga enlaces con palabras clave como "news", "noticia", "article", etc.

## Personalización

### Agregar un nuevo sitio web

1. Editar `scrapers.py` y agregar un nuevo método:
```python
def _scrapear_nuevo_sitio(self, soup, base_url):
    # Tu lógica de scraping aquí
    pass
```

2. Actualizar el método `_determinar_scraper`:
```python
elif 'nuevo-sitio.com' in domain:
    return self._scrapear_nuevo_sitio(soup, url)
```

### Modificar configuración

Editar `config.py` para cambiar:
- Timeouts
- Número máximo de noticias
- Palabras clave de filtrado
- Selectores CSS

## Estructura del modelo

```python
class Noticia:
    titulo: str          # Título de la noticia
    resumen: str         # Resumen/descripción
    imagen_preview: str  # URL de imagen de vista previa
    link: str           # Enlace a la noticia original
    fuente: str         # Fuente de la noticia
    fecha_publicacion: datetime  # Fecha de publicación
    fecha_scraping: datetime     # Fecha de scraping
```

## Manejo de errores

El sistema incluye manejo robusto de errores:
- Timeouts de conexión
- Sitios web no disponibles
- HTML malformado
- Enlaces rotos
- Duplicados

Todos los errores se registran en el log para facilitar el debugging.

## Consideraciones importantes

1. **Respeto a los sitios web**: El scraper incluye delays y user-agents apropiados
2. **Rate limiting**: No hagas demasiadas peticiones seguidas
3. **Términos de servicio**: Asegúrate de cumplir con los ToS de cada sitio
4. **Datos personales**: No extraigas información personal

## Troubleshooting

### Error: "No module named 'bs4'"
```bash
pip install beautifulsoup4
```

### Error: "No module named 'requests'"
```bash
pip install requests
```

### Error: "No module named 'rest_framework'"
```bash
pip install djangorestframework
```

### Las noticias no se extraen correctamente
1. Verifica que el sitio web esté disponible
2. Revisa los selectores CSS en el scraper específico
3. Comprueba los logs para errores específicos
