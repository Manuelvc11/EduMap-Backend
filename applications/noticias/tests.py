from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Noticia
from .scrapers import ScrapingManager
from unittest.mock import patch, Mock
import json


class NoticiaModelTest(TestCase):
    """Tests para el modelo Noticia"""
    
    def setUp(self):
        self.noticia = Noticia.objects.create(
            titulo="Test Noticia",
            resumen="Esta es una noticia de prueba",
            imagen_preview="https://example.com/image.jpg",
            link="https://example.com/noticia",
            fuente="Test Source"
        )
    
    def test_noticia_creation(self):
        """Test que verifica la creación de una noticia"""
        self.assertEqual(self.noticia.titulo, "Test Noticia")
        self.assertEqual(self.noticia.fuente, "Test Source")
        self.assertTrue(self.noticia.fecha_scraping is not None)
    
    def test_noticia_str_representation(self):
        """Test que verifica la representación string del modelo"""
        self.assertEqual(str(self.noticia), "Test Noticia")
    
    def test_noticia_str_representation_long_title(self):
        """Test que verifica el truncado de títulos largos"""
        long_title = "A" * 60
        noticia_larga = Noticia.objects.create(
            titulo=long_title,
            link="https://example.com/noticia2",
            fuente="Test Source"
        )
        self.assertEqual(str(noticia_larga), "A" * 50 + "...")


class NoticiaAPITest(APITestCase):
    """Tests para la API de noticias"""
    
    def setUp(self):
        # Crear algunas noticias de prueba
        Noticia.objects.create(
            titulo="Noticia 1",
            resumen="Resumen 1",
            link="https://example.com/1",
            fuente="Test Source 1"
        )
        Noticia.objects.create(
            titulo="Noticia 2",
            resumen="Resumen 2",
            link="https://example.com/2",
            fuente="Test Source 2"
        )
    
    def test_listar_noticias(self):
        """Test que verifica el listado de noticias"""
        url = reverse('noticias:listar_noticias')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['noticias']), 2)
        self.assertEqual(response.data['total'], 2)
    
    def test_listar_noticias_paginacion(self):
        """Test que verifica la paginación"""
        url = reverse('noticias:listar_noticias')
        response = self.client.get(url, {'page': 1, 'per_page': 1})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['noticias']), 1)
        self.assertEqual(response.data['total'], 2)
        self.assertEqual(response.data['total_pages'], 2)
    
    def test_noticia_detalle(self):
        """Test que verifica el detalle de una noticia"""
        noticia = Noticia.objects.first()
        url = reverse('noticias:noticia_detalle', kwargs={'noticia_id': noticia.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['titulo'], noticia.titulo)
    
    def test_noticia_detalle_no_existe(self):
        """Test que verifica el error cuando una noticia no existe"""
        url = reverse('noticias:noticia_detalle', kwargs={'noticia_id': 999})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_fuentes_disponibles(self):
        """Test que verifica el listado de fuentes"""
        url = reverse('noticias:fuentes_disponibles')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Test Source 1', response.data['fuentes'])
        self.assertIn('Test Source 2', response.data['fuentes'])


class ScrapingManagerTest(TestCase):
    """Tests para el ScrapingManager"""
    
    def setUp(self):
        self.scraper = ScrapingManager()
    
    def test_scraper_initialization(self):
        """Test que verifica la inicialización del scraper"""
        self.assertIsNotNone(self.scraper.headers)
        self.assertIn('User-Agent', self.scraper.headers)
    
    @patch('requests.get')
    def test_scrapear_sitio_exitoso(self, mock_get):
        """Test que verifica el scraping exitoso de un sitio"""
        # Mock de la respuesta HTTP
        mock_response = Mock()
        mock_response.content = """
        <html>
            <body>
                <article>
                    <h3>Título de prueba</h3>
                    <a href="/noticia">Enlace</a>
                    <p>Resumen de prueba</p>
                    <img src="/imagen.jpg">
                </article>
            </body>
        </html>
        """
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Mock del método _determinar_scraper
        with patch.object(self.scraper, '_determinar_scraper') as mock_determinar:
            mock_determinar.return_value = [{
                'titulo': 'Título de prueba',
                'resumen': 'Resumen de prueba',
                'imagen_preview': 'https://example.com/imagen.jpg',
                'link': 'https://example.com/noticia',
                'fecha_publicacion': None
            }]
            
            noticias = self.scraper.scrapear_sitio('https://example.com', 'Test Source')
            
            self.assertEqual(len(noticias), 1)
            self.assertEqual(noticias[0].titulo, 'Título de prueba')
            self.assertEqual(noticias[0].fuente, 'Test Source')
    
    @patch('requests.get')
    def test_scrapear_sitio_error_conexion(self, mock_get):
        """Test que verifica el manejo de errores de conexión"""
        mock_get.side_effect = Exception("Error de conexión")
        
        noticias = self.scraper.scrapear_sitio('https://example.com', 'Test Source')
        
        self.assertEqual(len(noticias), 0)
    
    def test_determinar_scraper_bbc(self):
        """Test que verifica la detección de BBC"""
        from bs4 import BeautifulSoup
        
        html = '<html><body><div class="gs-c-promo">Test</div></body></html>'
        soup = BeautifulSoup(html, 'html.parser')
        
        with patch.object(self.scraper, '_scrapear_bbc') as mock_bbc:
            mock_bbc.return_value = []
            self.scraper._determinar_scraper(soup, 'https://www.bbc.com/news', 'BBC')
            mock_bbc.assert_called_once()
    
    def test_determinar_scraper_cnn(self):
        """Test que verifica la detección de CNN"""
        from bs4 import BeautifulSoup
        
        html = '<html><body><article>Test</article></body></html>'
        soup = BeautifulSoup(html, 'html.parser')
        
        with patch.object(self.scraper, '_scrapear_cnn') as mock_cnn:
            mock_cnn.return_value = []
            self.scraper._determinar_scraper(soup, 'https://www.cnn.com', 'CNN')
            mock_cnn.assert_called_once()
    
    def test_determinar_scraper_generico(self):
        """Test que verifica el scraper genérico"""
        from bs4 import BeautifulSoup
        
        html = '<html><body><a href="/news/test">Test News</a></body></html>'
        soup = BeautifulSoup(html, 'html.parser')
        
        with patch.object(self.scraper, '_scrapear_generico') as mock_generico:
            mock_generico.return_value = []
            self.scraper._determinar_scraper(soup, 'https://example.com', 'Generic')
            mock_generico.assert_called_once()


class ScrapingAPITest(APITestCase):
    """Tests para la API de scraping"""
    
    @patch('applications.noticias.views.ScrapingManager')
    def test_scrapear_noticias_exitoso(self, mock_scraper_class):
        """Test que verifica el scraping exitoso via API"""
        # Mock del scraper
        mock_scraper = Mock()
        mock_scraper.scrapear_sitio.return_value = [
            Noticia(
                titulo="Noticia de prueba",
                resumen="Resumen de prueba",
                link="https://example.com/noticia",
                fuente="Test Source"
            )
        ]
        mock_scraper_class.return_value = mock_scraper
        
        url = reverse('noticias:scrapear_noticias')
        data = {
            'url': 'https://example.com',
            'fuente': 'Test Source'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('mensaje', response.data)
        self.assertIn('noticias', response.data)
    
    def test_scrapear_noticias_datos_invalidos(self):
        """Test que verifica el manejo de datos inválidos"""
        url = reverse('noticias:scrapear_noticias')
        data = {
            'url': 'url-invalida',
            'fuente': ''
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('url', response.data)
    
    @patch('applications.noticias.views.ScrapingManager')
    def test_scrapear_noticias_error_scraping(self, mock_scraper_class):
        """Test que verifica el manejo de errores en el scraping"""
        # Mock del scraper que lanza una excepción
        mock_scraper = Mock()
        mock_scraper.scrapear_sitio.side_effect = Exception("Error de scraping")
        mock_scraper_class.return_value = mock_scraper
        
        url = reverse('noticias:scrapear_noticias')
        data = {
            'url': 'https://example.com',
            'fuente': 'Test Source'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn('error', response.data)
