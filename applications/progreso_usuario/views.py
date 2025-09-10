from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from .models import ProgresoUsuario, LogProgreso
from .forms import ProgresoUsuarioForm


@login_required
def lista_progreso(request):
    """Vista para listar el progreso del usuario actual"""
    progresos = ProgresoUsuario.objects.filter(usuario=request.user)
    
    # Filtros
    actividad = request.GET.get('actividad')
    completado = request.GET.get('completado')
    
    if actividad:
        progresos = progresos.filter(actividad__icontains=actividad)
    if completado is not None:
        progresos = progresos.filter(completado=completado == 'true')
    
    # Paginación
    paginator = Paginator(progresos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'actividad': actividad,
        'completado': completado,
    }
    return render(request, 'progreso_usuario/lista.html', context)


@login_required
def detalle_progreso(request, pk):
    """Vista para mostrar el detalle de un progreso específico"""
    progreso = get_object_or_404(ProgresoUsuario, pk=pk, usuario=request.user)
    logs = LogProgreso.objects.filter(progreso_usuario=progreso)
    
    context = {
        'progreso': progreso,
        'logs': logs,
    }
    return render(request, 'progreso_usuario/detalle.html', context)


@login_required
def crear_progreso(request):
    """Vista para crear un nuevo progreso"""
    if request.method == 'POST':
        form = ProgresoUsuarioForm(request.POST)
        if form.is_valid():
            progreso = form.save(commit=False)
            progreso.usuario = request.user
            progreso.save()
            messages.success(request, 'Progreso creado exitosamente.')
            return redirect('progreso_usuario:detalle', pk=progreso.pk)
    else:
        form = ProgresoUsuarioForm()
    
    context = {'form': form}
    return render(request, 'progreso_usuario/crear.html', context)


@login_required
def editar_progreso(request, pk):
    """Vista para editar un progreso existente"""
    progreso = get_object_or_404(ProgresoUsuario, pk=pk, usuario=request.user)
    
    if request.method == 'POST':
        form = ProgresoUsuarioForm(request.POST, instance=progreso)
        if form.is_valid():
            # Guardar progreso anterior para el log
            progreso_anterior = progreso.progreso
            progreso = form.save()
            
            # Crear log si el progreso cambió
            if progreso_anterior != progreso.progreso:
                LogProgreso.objects.create(
                    progreso_usuario=progreso,
                    progreso_anterior=progreso_anterior,
                    progreso_nuevo=progreso.progreso,
                    descripcion=f"Progreso actualizado de {progreso_anterior}% a {progreso.progreso}%"
                )
            
            messages.success(request, 'Progreso actualizado exitosamente.')
            return redirect('progreso_usuario:detalle', pk=progreso.pk)
    else:
        form = ProgresoUsuarioForm(instance=progreso)
    
    context = {'form': form, 'progreso': progreso}
    return render(request, 'progreso_usuario/editar.html', context)


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


@login_required
def eliminar_progreso(request, pk):
    """Vista para eliminar un progreso"""
    progreso = get_object_or_404(ProgresoUsuario, pk=pk, usuario=request.user)
    
    if request.method == 'POST':
        progreso.delete()
        messages.success(request, 'Progreso eliminado exitosamente.')
        return redirect('progreso_usuario:lista')
    
    context = {'progreso': progreso}
    return render(request, 'progreso_usuario/eliminar.html', context)
