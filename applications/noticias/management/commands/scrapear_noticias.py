from django.core.management.base import BaseCommand, CommandError
from applications.noticias.scrapers import ScrapingManager
from applications.noticias.config import SITIOS_NOTICIAS
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Comando para realizar web scraping de noticias desde la línea de comandos'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--url',
            type=str,
            help='URL del sitio web a scrapear'
        )
        parser.add_argument(
            '--fuente',
            type=str,
            help='Nombre de la fuente de noticias'
        )
        parser.add_argument(
            '--sitio',
            type=str,
            choices=list(SITIOS_NOTICIAS.keys()),
            help='Sitio predefinido a scrapear'
        )
        parser.add_argument(
            '--todos',
            action='store_true',
            help='Scrapear todos los sitios predefinidos'
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Mostrar información detallada'
        )
    
    def handle(self, *args, **options):
        scraper = ScrapingManager()
        
        if options['verbose']:
            logging.basicConfig(level=logging.INFO)
        
        if options['todos']:
            self.scrapear_todos_los_sitios(scraper)
        elif options['sitio']:
            self.scrapear_sitio_predefinido(scraper, options['sitio'])
        elif options['url'] and options['fuente']:
            self.scrapear_url_personalizada(scraper, options['url'], options['fuente'])
        else:
            raise CommandError(
                'Debes especificar --url y --fuente, --sitio, o --todos'
            )
    
    def scrapear_todos_los_sitios(self, scraper):
        """Scrapea todos los sitios predefinidos"""
        self.stdout.write(
            self.style.SUCCESS('Iniciando scraping de todos los sitios predefinidos...')
        )
        
        total_noticias = 0
        
        for sitio_id, config in SITIOS_NOTICIAS.items():
            self.stdout.write(f'Scrapeando {config["nombre"]}...')
            
            for url in config['urls']:
                try:
                    noticias = scraper.scrapear_sitio(url, config['nombre'])
                    total_noticias += len(noticias)
                    
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'  ✓ {len(noticias)} noticias encontradas en {url}'
                        )
                    )
                    
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'  ✗ Error en {url}: {str(e)}')
                    )
        
        self.stdout.write(
            self.style.SUCCESS(f'Scraping completado. Total: {total_noticias} noticias')
        )
    
    def scrapear_sitio_predefinido(self, scraper, sitio_id):
        """Scrapea un sitio predefinido"""
        if sitio_id not in SITIOS_NOTICIAS:
            raise CommandError(f'Sitio "{sitio_id}" no encontrado')
        
        config = SITIOS_NOTICIAS[sitio_id]
        self.stdout.write(f'Scrapeando {config["nombre"]}...')
        
        total_noticias = 0
        
        for url in config['urls']:
            try:
                noticias = scraper.scrapear_sitio(url, config['nombre'])
                total_noticias += len(noticias)
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'  ✓ {len(noticias)} noticias encontradas en {url}'
                    )
                )
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'  ✗ Error en {url}: {str(e)}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'Scraping completado. Total: {total_noticias} noticias')
        )
    
    def scrapear_url_personalizada(self, scraper, url, fuente):
        """Scrapea una URL personalizada"""
        self.stdout.write(f'Scrapeando {url} (Fuente: {fuente})...')
        
        try:
            noticias = scraper.scrapear_sitio(url, fuente)
            
            self.stdout.write(
                self.style.SUCCESS(f'✓ {len(noticias)} noticias encontradas')
            )
            
            # Mostrar detalles de las noticias si hay pocas
            if len(noticias) <= 5:
                for i, noticia in enumerate(noticias, 1):
                    self.stdout.write(f'  {i}. {noticia.titulo}')
            
        except Exception as e:
            raise CommandError(f'Error durante el scraping: {str(e)}')
