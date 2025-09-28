"""
Configuración para sitios web de noticias que se pueden scrapear.
Fácil de modificar y extender para principiantes.
"""

# Configuración de sitios web de noticias populares
SITIOS_NOTICIAS = {
    'bbc': {
        'nombre': 'BBC News',
        'urls': [
            'https://www.bbc.com/news',
            'https://www.bbc.com/news/world',
            'https://www.bbc.com/news/technology'
        ],
        'selectores': {
            'articulos': 'article, .gs-c-promo',
            'titulo': 'h3, h2, .gs-c-promo-heading',
            'enlace': 'a',
            'resumen': 'p.gs-c-promo-summary',
            'imagen': 'img'
        }
    },
    'cnn': {
        'nombre': 'CNN',
        'urls': [
            'https://www.cnn.com/',
            'https://www.cnn.com/world',
            'https://www.cnn.com/technology'
        ],
        'selectores': {
            'articulos': 'article, .cnn-search__result',
            'titulo': 'h3, h2',
            'enlace': 'a',
            'resumen': 'p',
            'imagen': 'img'
        }
    },
    'elpais': {
        'nombre': 'El País',
        'urls': [
            'https://elpais.com/',
            'https://elpais.com/internacional/',
            'https://elpais.com/tecnologia/'
        ],
        'selectores': {
            'articulos': 'article, .articulo',
            'titulo': 'h2, h3',
            'enlace': 'a',
            'resumen': 'p',
            'imagen': 'img'
        }
    },
    'marca': {
        'nombre': 'UDEA',
        'urls': [
            'https://www.udea.edu.co/wps/portal/udea/web/inicio/udea-noticias/noticias-academia',
            'https://www.udea.edu.co/wps/portal/udea/web/inicio/udea-noticias/udea-noticia/Contenido/asNoticias/Cultura/museo-abierto-alianza-udea-upv',
            'https://www.udea.edu.co/wps/portal/udea/web/inicio/udea-noticias/udea-noticia/Contenido/asNoticias/PeriodicoAlmaMater/andreu-guzman'
        ],
        'selectores': {
            'articulos': 'article, .modulo',
            'titulo': 'h2, h3',
            'enlace': 'a',
            'resumen': 'p',
            'imagen': 'img'
        }
    }
}

# Configuración de scraping
SCRAPING_CONFIG = {
    'timeout': 10,  # Timeout en segundos para las peticiones
    'max_noticias': 20,  # Máximo número de noticias a extraer por sitio
    'delay': 1,  # Delay entre peticiones (en segundos)
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Palabras clave para filtrar noticias relevantes
PALABRAS_CLAVE = [
    'tecnología', 'technology', 'ciencia', 'science',
    'educación', 'education', 'innovación', 'innovation',
    'digital', 'online', 'aprendizaje', 'learning',
    'universidad', 'university', 'estudiante', 'student'
]

# Configuración de logging
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
}
