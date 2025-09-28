from django.contrib import admin
from .models import Noticia


@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'fuente', 'fecha_publicacion', 'fecha_scraping']
    list_filter = ['fuente', 'fecha_publicacion']
    search_fields = ['titulo', 'resumen']
    readonly_fields = ['fecha_scraping']
    ordering = ['-fecha_publicacion']
