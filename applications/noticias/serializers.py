from rest_framework import serializers
from .models import Noticia


class NoticiaSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Noticia"""
    
    class Meta:
        model = Noticia
        fields = [
            'id',
            'titulo',
            'resumen',
            'imagen_preview',
            'link',
            'fuente',
            'fecha_publicacion',
            'fecha_scraping'
        ]
        read_only_fields = ['id', 'fecha_scraping']


class ScrapingRequestSerializer(serializers.Serializer):
    """Serializador para solicitudes de scraping"""
    url = serializers.URLField(help_text="URL del sitio web a scrapear")
    fuente = serializers.CharField(max_length=200, help_text="Nombre de la fuente de noticias")
