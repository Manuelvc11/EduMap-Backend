from django.urls import path
from . import views

app_name = 'noticias'

urlpatterns = [
    # Listar todas las noticias
    path('', views.listar_noticias, name='listar_noticias'),
    
    # Realizar scraping de noticias
    path('scrapear/', views.scrapear_noticias, name='scrapear_noticias'),
    
    # Detalle de una noticia específica
    path('<int:noticia_id>/', views.noticia_detalle, name='noticia_detalle'),
    
    # Listar fuentes disponibles
    path('fuentes/', views.fuentes_disponibles, name='fuentes_disponibles'),
]
