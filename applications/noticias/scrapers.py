"""
Módulo para realizar web scraping de noticias de diferentes sitios web.
Diseñado para ser fácil de entender y extender para principiantes.
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from django.utils import timezone
from datetime import datetime
import logging
from .models import Noticia

logger = logging.getLogger(__name__)


class ScrapingManager:
    """Manager principal para el web scraping de noticias"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def scrapear_sitio(self, url, fuente):
        """
        Método principal para scrapear un sitio web
        Args:
            url (str): URL del sitio a scrapear
            fuente (str): Nombre de la fuente
        Returns:
            list: Lista de noticias encontradas
        """
        try:
            # Obtener el contenido HTML del sitio
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            # Parsear el HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Determinar el tipo de sitio y usar el scraper apropiado
            noticias = self._determinar_scraper(soup, url, fuente)
            
            # Guardar las noticias en la base de datos
            noticias_guardadas = []
            for noticia_data in noticias:
                noticia, created = Noticia.objects.get_or_create(
                    link=noticia_data['link'],
                    fuente=fuente,
                    defaults=noticia_data
                )
                if created:
                    noticias_guardadas.append(noticia)
            
            return noticias_guardadas
            
        except Exception as e:
            logger.error(f"Error al scrapear {url}: {str(e)}")
            return []
    
    def _determinar_scraper(self, soup, url, fuente):
        """
        Determina qué scraper usar basado en el dominio o estructura del sitio
        """
        domain = urlparse(url).netloc.lower()
        
        # Scrapers específicos para sitios conocidos
        if 'bbc.com' in domain or 'bbc.co.uk' in domain:
            return self._scrapear_bbc(soup, url)
        elif 'cnn.com' in domain:
            return self._scrapear_cnn(soup, url)
        elif 'elpais.com' in domain:
            return self._scrapear_elpais(soup, url)
        elif 'marca.com' in domain:
            return self._scrapear_marca(soup, url)
        else:
            # Scraper genérico para sitios desconocidos
            return self._scrapear_generico(soup, url)
    
    def _scrapear_bbc(self, soup, base_url):
        """Scraper específico para BBC News"""
        noticias = []
        
        # Buscar artículos de noticias
        articles = soup.find_all('article') or soup.find_all('div', class_='gs-c-promo')
        
        for article in articles[:10]:  # Limitar a 10 noticias
            try:
                # Título
                title_elem = article.find('h3') or article.find('h2') or article.find('a', class_='gs-c-promo-heading')
                if not title_elem:
                    continue
                
                title = title_elem.get_text(strip=True)
                if not title:
                    continue
                
                # Enlace
                link_elem = article.find('a')
                if not link_elem or not link_elem.get('href'):
                    continue
                
                link = urljoin(base_url, link_elem['href'])
                
                # Resumen
                summary_elem = article.find('p', class_='gs-c-promo-summary')
                summary = summary_elem.get_text(strip=True) if summary_elem else ""
                
                # Imagen
                img_elem = article.find('img')
                image_url = img_elem.get('src') if img_elem else None
                if image_url and not image_url.startswith('http'):
                    image_url = urljoin(base_url, image_url)
                
                noticias.append({
                    'titulo': title,
                    'resumen': summary,
                    'imagen_preview': image_url,
                    'link': link,
                    'fecha_publicacion': timezone.now()
                })
                
            except Exception as e:
                logger.warning(f"Error al procesar artículo BBC: {str(e)}")
                continue
        
        return noticias
    
    def _scrapear_cnn(self, soup, base_url):
        """Scraper específico para CNN"""
        noticias = []
        
        # Buscar artículos de CNN
        articles = soup.find_all('article') or soup.find_all('div', class_='cnn-search__result')
        
        for article in articles[:10]:
            try:
                # Título
                title_elem = article.find('h3') or article.find('h2')
                if not title_elem:
                    continue
                
                title = title_elem.get_text(strip=True)
                if not title:
                    continue
                
                # Enlace
                link_elem = article.find('a')
                if not link_elem or not link_elem.get('href'):
                    continue
                
                link = urljoin(base_url, link_elem['href'])
                
                # Resumen
                summary_elem = article.find('p')
                summary = summary_elem.get_text(strip=True) if summary_elem else ""
                
                # Imagen
                img_elem = article.find('img')
                image_url = img_elem.get('src') if img_elem else None
                if image_url and not image_url.startswith('http'):
                    image_url = urljoin(base_url, image_url)
                
                noticias.append({
                    'titulo': title,
                    'resumen': summary,
                    'imagen_preview': image_url,
                    'link': link,
                    'fecha_publicacion': timezone.now()
                })
                
            except Exception as e:
                logger.warning(f"Error al procesar artículo CNN: {str(e)}")
                continue
        
        return noticias
    
    def _scrapear_elpais(self, soup, base_url):
        """Scraper específico para El País"""
        noticias = []
        
        # Buscar artículos de El País
        articles = soup.find_all('article') or soup.find_all('div', class_='articulo')
        
        for article in articles[:10]:
            try:
                # Título
                title_elem = article.find('h2') or article.find('h3')
                if not title_elem:
                    continue
                
                title = title_elem.get_text(strip=True)
                if not title:
                    continue
                
                # Enlace
                link_elem = article.find('a')
                if not link_elem or not link_elem.get('href'):
                    continue
                
                link = urljoin(base_url, link_elem['href'])
                
                # Resumen
                summary_elem = article.find('p')
                summary = summary_elem.get_text(strip=True) if summary_elem else ""
                
                # Imagen
                img_elem = article.find('img')
                image_url = img_elem.get('src') if img_elem else None
                if image_url and not image_url.startswith('http'):
                    image_url = urljoin(base_url, image_url)
                
                noticias.append({
                    'titulo': title,
                    'resumen': summary,
                    'imagen_preview': image_url,
                    'link': link,
                    'fecha_publicacion': timezone.now()
                })
                
            except Exception as e:
                logger.warning(f"Error al procesar artículo El País: {str(e)}")
                continue
        
        return noticias
    
    def _scrapear_udea(self, soup, base_url):
        """Scraper específico para Marca"""
        noticias = []
        
        # Buscar artículos de Marca
        articles = soup.find_all('article') or soup.find_all('div', class_='modulo')
        
        for article in articles[:10]:
            try:
                # Título
                title_elem = article.find('h2') or article.find('h3')
                if not title_elem:
                    continue
                
                title = title_elem.get_text(strip=True)
                if not title:
                    continue
                
                # Enlace
                link_elem = article.find('a')
                if not link_elem or not link_elem.get('href'):
                    continue
                
                link = urljoin(base_url, link_elem['href'])
                
                # Resumen
                summary_elem = article.find('p')
                summary = summary_elem.get_text(strip=True) if summary_elem else ""
                
                # Imagen
                img_elem = article.find('img')
                image_url = img_elem.get('src') if img_elem else None
                if image_url and not image_url.startswith('http'):
                    image_url = urljoin(base_url, image_url)
                
                noticias.append({
                    'titulo': title,
                    'resumen': summary,
                    'imagen_preview': image_url,
                    'link': link,
                    'fecha_publicacion': timezone.now()
                })
                
            except Exception as e:
                logger.warning(f"Error al procesar artículo Marca: {str(e)}")
                continue
        
        return noticias
    
    def _scrapear_generico(self, soup, base_url):
        """Scraper genérico para sitios desconocidos"""
        noticias = []
        
        # Buscar enlaces que parezcan noticias
        links = soup.find_all('a', href=True)
        
        for link in links[:20]:  # Limitar a 20 enlaces
            try:
                href = link.get('href')
                if not href:
                    continue
                
                # Filtrar enlaces que parezcan noticias
                if any(keyword in href.lower() for keyword in ['news', 'noticia', 'article', 'articulo']):
                    full_url = urljoin(base_url, href)
                    
                    # Obtener el texto del enlace como título
                    title = link.get_text(strip=True)
                    if len(title) < 10:  # Filtrar títulos muy cortos
                        continue
                    
                    # Buscar resumen en el elemento padre
                    parent = link.parent
                    summary = ""
                    if parent:
                        summary_elem = parent.find('p')
                        if summary_elem:
                            summary = summary_elem.get_text(strip=True)
                    
                    # Buscar imagen
                    img_elem = link.find('img') or (link.parent.find('img') if link.parent else None)
                    image_url = None
                    if img_elem:
                        image_url = img_elem.get('src')
                        if image_url and not image_url.startswith('http'):
                            image_url = urljoin(base_url, image_url)
                    
                    noticias.append({
                        'titulo': title,
                        'resumen': summary,
                        'imagen_preview': image_url,
                        'link': full_url,
                        'fecha_publicacion': timezone.now()
                    })
                
            except Exception as e:
                logger.warning(f"Error al procesar enlace genérico: {str(e)}")
                continue
        
        return noticias
