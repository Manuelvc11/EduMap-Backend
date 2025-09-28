from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.shortcuts import render
from django.http import JsonResponse
from .models import Noticia
from .serializers import NoticiaSerializer, ScrapingRequestSerializer
from .scrapers import ScrapingManager
import logging

logger = logging.getLogger(__name__)


@api_view(['GET'])
@permission_classes([AllowAny])
def listar_noticias(request):
    """Lista todas las noticias con paginación"""
    try:
        noticias = Noticia.objects.all().order_by('-fecha_publicacion')
        
        # Paginación simple
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 10))
        
        start = (page - 1) * per_page
        end = start + per_page
        
        noticias_paginated = noticias[start:end]
        
        serializer = NoticiaSerializer(noticias_paginated, many=True)
        
        return Response({
            'noticias': serializer.data,
            'total': noticias.count(),
            'page': page,
            'per_page': per_page,
            'total_pages': (noticias.count() + per_page - 1) // per_page
        })
    
    except Exception as e:
        logger.error(f"Error al listar noticias: {str(e)}")
        return Response(
            {'error': 'Error interno del servidor'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def scrapear_noticias(request):
    """Endpoint para realizar web scraping de noticias"""
    try:
        serializer = ScrapingRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        url = serializer.validated_data['url']
        fuente = serializer.validated_data['fuente']
        
        # Inicializar el manager de scraping
        scraper = ScrapingManager()
        
        # Realizar el scraping
        noticias_scraped = scraper.scrapear_sitio(url, fuente)
        
        if not noticias_scraped:
            return Response(
                {'mensaje': 'No se encontraron noticias en el sitio especificado'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Serializar las noticias encontradas
        noticias_serializer = NoticiaSerializer(noticias_scraped, many=True)
        
        return Response({
            'mensaje': f'Se encontraron {len(noticias_scraped)} noticias',
            'noticias': noticias_serializer.data
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        logger.error(f"Error en scraping: {str(e)}")
        return Response(
            {'error': f'Error durante el scraping: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def noticia_detalle(request, noticia_id):
    """Obtiene los detalles de una noticia específica"""
    try:
        noticia = Noticia.objects.get(id=noticia_id)
        serializer = NoticiaSerializer(noticia)
        return Response(serializer.data)
    
    except Noticia.DoesNotExist:
        return Response(
            {'error': 'Noticia no encontrada'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    except Exception as e:
        logger.error(f"Error al obtener noticia: {str(e)}")
        return Response(
            {'error': 'Error interno del servidor'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def fuentes_disponibles(request):
    """Lista las fuentes de noticias disponibles"""
    try:
        fuentes = Noticia.objects.values_list('fuente', flat=True).distinct()
        return Response({'fuentes': list(fuentes)})
    
    except Exception as e:
        logger.error(f"Error al obtener fuentes: {str(e)}")
        return Response(
            {'error': 'Error interno del servidor'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
