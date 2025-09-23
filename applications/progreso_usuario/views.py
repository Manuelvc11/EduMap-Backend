from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from .models import ProgresoUsuario, LogProgreso
from .forms import ProgresoUsuarioForm


@csrf_exempt
@login_required
def lista_progreso(request):
    """API para listar el progreso del usuario actual"""
    try:
        progresos = ProgresoUsuario.objects.filter(usuario=request.user)
        
        actividad = request.GET.get('actividad')
        completado = request.GET.get('completado')
        
        if actividad:
            progresos = progresos.filter(actividad__icontains=actividad)
        if completado is not None:
            progresos = progresos.filter(completado=completado == 'true')

        paginator = Paginator(progresos, 10)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        
        progresos_data = []
        for progreso in page_obj:
            progresos_data.append({
                'id': progreso.id,
                'actividad': progreso.actividad,
                'progreso': float(progreso.progreso),
                'completado': progreso.completado,
                'fecha_inicio': progreso.fecha_inicio.isoformat(),
                'fecha_actualizacion': progreso.fecha_actualizacion.isoformat(),
                'resultado': progreso.resultado
            })
        
        return JsonResponse({
            'success': True,
            'progresos': progresos_data,
            'pagination': {
                'current_page': page_obj.number,
                'total_pages': paginator.num_pages,
                'total_items': paginator.count,
                'has_next': page_obj.has_next(),
                'has_previous': page_obj.has_previous(),
                'next_page': page_obj.next_page_number() if page_obj.has_next() else None,
                'previous_page': page_obj.previous_page_number() if page_obj.has_previous() else None
            },
            'filters': {
                'actividad': actividad,
                'completado': completado
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al obtener lista de progreso: {str(e)}'
        }, status=500)


@csrf_exempt
@login_required
def detalle_progreso(request, pk):
    """API para mostrar el detalle de un progreso específico"""
    try:
        progreso = get_object_or_404(ProgresoUsuario, pk=pk, usuario=request.user)
        logs = LogProgreso.objects.filter(progreso_usuario=progreso)
        
        # Convertir logs a formato JSON
        logs_data = []
        for log in logs:
            logs_data.append({
                'id': log.id,
                'progreso_anterior': float(log.progreso_anterior),
                'progreso_nuevo': float(log.progreso_nuevo),
                'descripcion': log.descripcion,
                'fecha_cambio': log.fecha_cambio.isoformat()
            })
        
        progreso_data = {
            'id': progreso.id,
            'actividad': progreso.actividad,
            'progreso': float(progreso.progreso),
            'completado': progreso.completado,
            'fecha_inicio': progreso.fecha_inicio.isoformat(),
            'fecha_actualizacion': progreso.fecha_actualizacion.isoformat(),
            'resultado': progreso.resultado,
            'logs': logs_data
        }
        
        return JsonResponse({
            'success': True,
            'progreso': progreso_data
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al obtener detalle del progreso: {str(e)}'
        }, status=500)


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def crear_progreso(request):
    """API para crear un nuevo progreso"""
    try:
        import json
        data = json.loads(request.body)
        
        required_fields = ['actividad', 'progreso']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({
                    'success': False,
                    'message': f'El campo {field} es requerido'
                }, status=400)
        
        progreso = ProgresoUsuario.objects.create(
            usuario=request.user,
            actividad=data['actividad'],
            progreso=float(data['progreso']),
            completado=float(data['progreso']) >= 100,
            resultado=data.get('resultado', '')
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Progreso creado exitosamente',
            'progreso': {
                'id': progreso.id,
                'actividad': progreso.actividad,
                'progreso': float(progreso.progreso),
                'completado': progreso.completado,
                'fecha_inicio': progreso.fecha_inicio.isoformat(),
                'fecha_actualizacion': progreso.fecha_actualizacion.isoformat(),
                'resultado': progreso.resultado
            }
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'JSON inválido'
        }, status=400)
    except ValueError as e:
        return JsonResponse({
            'success': False,
            'message': f'Error en los datos: {str(e)}'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al crear progreso: {str(e)}'
        }, status=500)


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def editar_progreso(request, pk):
    """API para editar un progreso existente"""
    try:
        import json
        data = json.loads(request.body)
        progreso = get_object_or_404(ProgresoUsuario, pk=pk, usuario=request.user)
        
        progreso_anterior = progreso.progreso
        
        progreso.actividad = data.get('actividad', progreso.actividad)
        progreso.progreso = float(data.get('progreso', progreso.progreso))
        progreso.completado = progreso.progreso >= 100
        progreso.resultado = data.get('resultado', progreso.resultado)
        
        progreso.save()
        
        if progreso_anterior != progreso.progreso:
            LogProgreso.objects.create(
                progreso_usuario=progreso,
                progreso_anterior=progreso_anterior,
                progreso_nuevo=progreso.progreso,
                descripcion=f"Progreso actualizado de {progreso_anterior}% a {progreso.progreso}%"
            )
        
        return JsonResponse({
            'success': True,
            'message': 'Progreso actualizado exitosamente',
            'progreso': {
                'id': progreso.id,
                'actividad': progreso.actividad,
                'progreso': float(progreso.progreso),
                'completado': progreso.completado,
                'fecha_inicio': progreso.fecha_inicio.isoformat(),
                'fecha_actualizacion': progreso.fecha_actualizacion.isoformat(),
                'resultado': progreso.resultado
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'JSON inválido'
        }, status=400)
    except ValueError as e:
        return JsonResponse({
            'success': False,
            'message': f'Error en los datos: {str(e)}'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al editar progreso: {str(e)}'
        }, status=500)


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def actualizar_progreso_ajax(request, pk):
    """Vista AJAX para actualizar progreso rápidamente"""
    progreso = get_object_or_404(ProgresoUsuario, pk=pk, usuario=request.user)
    
    nuevo_progreso = request.POST.get('progreso')
    if nuevo_progreso is not None:
        try:
            progreso_anterior = progreso.progreso
            progreso.progreso = float(nuevo_progreso)
            progreso.completado = progreso.progreso >= 100
            progreso.save()
            
            # Crear log
            LogProgreso.objects.create(
                progreso_usuario=progreso,
                progreso_anterior=progreso_anterior,
                progreso_nuevo=progreso.progreso,
                descripcion="Progreso actualizado vía AJAX"
            )
            
            return JsonResponse({
                'success': True,
                'progreso': float(progreso.progreso),
                'completado': progreso.completado
            })
        except ValueError:
            return JsonResponse({'success': False, 'error': 'Valor de progreso inválido'})
    
    return JsonResponse({'success': False, 'error': 'Progreso no proporcionado'})


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def eliminar_progreso(request, pk):
    """API para eliminar un progreso"""
    try:
        progreso = get_object_or_404(ProgresoUsuario, pk=pk, usuario=request.user)
        progreso.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Progreso eliminado exitosamente'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al eliminar progreso: {str(e)}'
        }, status=500)
