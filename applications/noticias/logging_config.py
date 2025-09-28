"""
Configuración de logging para el sistema de web scraping.
"""

import logging
import os
from django.conf import settings

def setup_scraping_logging():
    """Configura el logging para el sistema de scraping"""
    
    # Crear directorio de logs si no existe
    log_dir = os.path.join(settings.BASE_DIR, 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Configurar el logger principal
    logger = logging.getLogger('scraping')
    logger.setLevel(logging.INFO)
    
    # Evitar duplicar handlers
    if not logger.handlers:
        # Handler para archivo
        file_handler = logging.FileHandler(
            os.path.join(log_dir, 'scraping.log'),
            encoding='utf-8'
        )
        file_handler.setLevel(logging.INFO)
        
        # Handler para consola
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        
        # Formato de los logs
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Agregar handlers al logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger

def get_scraping_logger():
    """Obtiene el logger configurado para scraping"""
    return logging.getLogger('scraping')
