from django.db import models
from django.utils import timezone


class Noticia(models.Model):
    """Modelo para almacenar noticias obtenidas mediante web scraping"""
    
    titulo = models.CharField(max_length=500, verbose_name="Título")
    resumen = models.TextField(verbose_name="Resumen", blank=True, null=True)
    imagen_preview = models.URLField(max_length=1000, verbose_name="Imagen de vista previa", blank=True, null=True)
    link = models.URLField(max_length=1000, verbose_name="Enlace a la noticia")
    fuente = models.CharField(max_length=200, verbose_name="Fuente de la noticia")
    fecha_publicacion = models.DateTimeField(verbose_name="Fecha de publicación", blank=True, null=True)
    fecha_scraping = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de scraping")
    
    class Meta:
        verbose_name = "Noticia"
        verbose_name_plural = "Noticias"
        ordering = ['-fecha_publicacion']
        unique_together = ['link', 'fuente']  # Evita duplicados
    
    def __str__(self):
        return self.titulo[:50] + "..." if len(self.titulo) > 50 else self.titulo
