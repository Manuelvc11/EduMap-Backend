#!/usr/bin/env python3
"""
Ejemplo de uso del sistema de web scraping de noticias.
Este archivo muestra cómo usar la API desde Python.
"""

import requests
import json
from datetime import datetime

# Configuración de la API
API_BASE_URL = "http://localhost:8000/api/noticias"

def ejemplo_scrapear_bbc():
    """Ejemplo de cómo scrapear noticias de BBC"""
    print("🔍 Scrapeando noticias de BBC...")
    
    url = f"{API_BASE_URL}/scrapear/"
    data = {
        "url": "https://www.bbc.com/news",
        "fuente": "BBC News"
    }
    
    try:
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ {result['mensaje']}")
            
            # Mostrar las primeras 3 noticias
            for i, noticia in enumerate(result['noticias'][:3], 1):
                print(f"\n{i}. {noticia['titulo']}")
                print(f"   Fuente: {noticia['fuente']}")
                print(f"   Enlace: {noticia['link']}")
        else:
            print(f"❌ Error: {response.json()}")
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

def ejemplo_scrapear_cnn():
    """Ejemplo de cómo scrapear noticias de CNN"""
    print("\n🔍 Scrapeando noticias de CNN...")
    
    url = f"{API_BASE_URL}/scrapear/"
    data = {
        "url": "https://www.cnn.com/",
        "fuente": "CNN"
    }
    
    try:
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ {result['mensaje']}")
        else:
            print(f"❌ Error: {response.json()}")
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

def ejemplo_listar_noticias():
    """Ejemplo de cómo listar noticias con paginación"""
    print("\n📰 Listando noticias...")
    
    url = f"{API_BASE_URL}/"
    params = {
        "page": 1,
        "per_page": 5
    }
    
    try:
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            result = response.json()
            print(f"📊 Total de noticias: {result['total']}")
            print(f"📄 Página {result['page']} de {result['total_pages']}")
            
            for i, noticia in enumerate(result['noticias'], 1):
                print(f"\n{i}. {noticia['titulo']}")
                print(f"   Fuente: {noticia['fuente']}")
                print(f"   Fecha: {noticia['fecha_publicacion']}")
        else:
            print(f"❌ Error: {response.json()}")
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

def ejemplo_fuentes_disponibles():
    """Ejemplo de cómo obtener fuentes disponibles"""
    print("\n📋 Obteniendo fuentes disponibles...")
    
    url = f"{API_BASE_URL}/fuentes/"
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            result = response.json()
            print("📰 Fuentes disponibles:")
            for fuente in result['fuentes']:
                print(f"   • {fuente}")
        else:
            print(f"❌ Error: {response.json()}")
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

def ejemplo_scrapear_sitio_personalizado():
    """Ejemplo de cómo scrapear un sitio personalizado"""
    print("\n🔍 Scrapeando sitio personalizado...")
    
    url = f"{API_BASE_URL}/scrapear/"
    data = {
        "url": "https://elpais.com/",
        "fuente": "El País"
    }
    
    try:
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ {result['mensaje']}")
        else:
            print(f"❌ Error: {response.json()}")
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

def main():
    """Función principal que ejecuta todos los ejemplos"""
    print("🚀 Ejemplo de uso del sistema de web scraping de noticias")
    print("=" * 60)
    
    # Verificar que el servidor esté funcionando
    try:
        response = requests.get(f"{API_BASE_URL}/")
        if response.status_code != 200:
            print("❌ El servidor no está funcionando. Asegúrate de que Django esté ejecutándose.")
            return
    except:
        print("❌ No se puede conectar al servidor. Asegúrate de que Django esté ejecutándose.")
        return
    
    # Ejecutar ejemplos
    ejemplo_scrapear_bbc()
    ejemplo_scrapear_cnn()
    ejemplo_scrapear_sitio_personalizado()
    ejemplo_listar_noticias()
    ejemplo_fuentes_disponibles()
    
    print("\n" + "=" * 60)
    print("✅ Ejemplos completados!")

if __name__ == "__main__":
    main()
