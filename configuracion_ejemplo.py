#!/usr/bin/env python3
"""
Archivo de configuración de ejemplo para el sistema de web scraping.
Copia este archivo y modifícalo según tus necesidades.
"""

# URLs de sitios web de noticias populares
SITIOS_NOTICIAS_EJEMPLO = {
    'bbc_espanol': {
        'nombre': 'BBC Mundo',
        'urls': [
            'https://www.bbc.com/mundo',
            'https://www.bbc.com/mundo/noticias',
            'https://www.bbc.com/mundo/tecnologia'
        ]
    },
    'cnn_espanol': {
        'nombre': 'CNN en Español',
        'urls': [
            'https://cnnespanol.cnn.com/',
            'https://cnnespanol.cnn.com/tecnologia/',
            'https://cnnespanol.cnn.com/educacion/'
        ]
    },
    'el_pais': {
        'nombre': 'El País',
        'urls': [
            'https://elpais.com/',
            'https://elpais.com/tecnologia/',
            'https://elpais.com/educacion/'
        ]
    },
    'marca': {
        'nombre': 'Marca',
        'urls': [
            'https://www.marca.com/',
            'https://www.marca.com/futbol/',
            'https://www.marca.com/baloncesto/'
        ]
    },
    'xataka': {
        'nombre': 'Xataka',
        'urls': [
            'https://www.xataka.com/',
            'https://www.xataka.com/tecnologia/',
            'https://www.xataka.com/educacion/'
        ]
    }
}

# Configuración de scraping personalizada
CONFIGURACION_SCRAPING = {
    'timeout': 15,  # Timeout en segundos
    'max_noticias_por_sitio': 25,  # Máximo de noticias por sitio
    'delay_entre_peticiones': 2,  # Delay entre peticiones (segundos)
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'headers_adicionales': {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
}

# Palabras clave para filtrar noticias relevantes
PALABRAS_CLAVE_FILTRO = [
    # Tecnología
    'tecnología', 'technology', 'tech', 'digital', 'innovación', 'innovation',
    'inteligencia artificial', 'artificial intelligence', 'AI', 'machine learning',
    'programación', 'programming', 'software', 'hardware', 'internet',
    
    # Educación
    'educación', 'education', 'aprendizaje', 'learning', 'estudiante', 'student',
    'universidad', 'university', 'colegio', 'school', 'profesor', 'teacher',
    'curso', 'course', 'formación', 'training', 'académico', 'academic',
    
    # Ciencia
    'ciencia', 'science', 'investigación', 'research', 'estudio', 'study',
    'descubrimiento', 'discovery', 'experimento', 'experiment',
    
    # Noticias generales
    'noticia', 'news', 'actualidad', 'current', 'tendencia', 'trend',
    'análisis', 'analysis', 'reportaje', 'report', 'artículo', 'article'
]

# Configuración de logging
CONFIGURACION_LOGGING = {
    'nivel': 'INFO',  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    'formato': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'archivo_log': 'logs/scraping.log',
    'max_tamaño_archivo': 10 * 1024 * 1024,  # 10MB
    'numero_archivos_respaldo': 5
}

# Configuración de la base de datos
CONFIGURACION_BD = {
    'limpiar_noticias_antiguas': True,
    'dias_antiguedad_maxima': 30,  # Días después de los cuales eliminar noticias
    'limite_noticias_por_fuente': 1000,  # Máximo de noticias por fuente
}

# Configuración de la API
CONFIGURACION_API = {
    'paginacion_default': 10,
    'paginacion_maxima': 100,
    'rate_limiting': True,
    'max_requests_por_minuto': 60,
    'cors_origins': ['http://localhost:3000', 'http://127.0.0.1:3000']
}

# Ejemplo de uso de la configuración
def ejemplo_uso_configuracion():
    """Muestra cómo usar esta configuración"""
    print("🔧 Configuración de ejemplo para web scraping")
    print("=" * 50)
    
    print(f"📰 Sitios configurados: {len(SITIOS_NOTICIAS_EJEMPLO)}")
    for sitio_id, config in SITIOS_NOTICIAS_EJEMPLO.items():
        print(f"   • {config['nombre']}: {len(config['urls'])} URLs")
    
    print(f"\n⚙️ Configuración de scraping:")
    print(f"   • Timeout: {CONFIGURACION_SCRAPING['timeout']}s")
    print(f"   • Max noticias por sitio: {CONFIGURACION_SCRAPING['max_noticias_por_sitio']}")
    print(f"   • Delay entre peticiones: {CONFIGURACION_SCRAPING['delay_entre_peticiones']}s")
    
    print(f"\n🔍 Palabras clave de filtro: {len(PALABRAS_CLAVE_FILTRO)}")
    print(f"   • Ejemplos: {', '.join(PALABRAS_CLAVE_FILTRO[:5])}...")
    
    print(f"\n📊 Configuración de BD:")
    print(f"   • Limpiar noticias antiguas: {CONFIGURACION_BD['limpiar_noticias_antiguas']}")
    print(f"   • Días de antigüedad máxima: {CONFIGURACION_BD['dias_antiguedad_maxima']}")

if __name__ == "__main__":
    ejemplo_uso_configuracion()
