from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import json
from .forms import FormularioRegistroPersonalizado, FormularioPerfilUsuario
from .models import PerfilUsuario, Usuario


def vista_home(request):
    """
    Vista de página principal que devuelve información de la API
    """
    return JsonResponse({
        'success': True,
        'message': '¡Bienvenido a EduMap API!',
        'version': '1.0.0',
        'endpoints': {
            'usuarios': {
                'login': '/api/usuarios/login/',
                'logout': '/api/usuarios/logout/',
                'register': '/api/usuarios/register/',
                'dashboard': '/api/usuarios/dashboard/',
                'profile': '/api/usuarios/profile/'
            },
            'progreso': {
                'lista': '/api/progreso/',
                'crear': '/api/progreso/crear/',
                'detalle': '/api/progreso/<id>/',
                'editar': '/api/progreso/<id>/editar/',
                'eliminar': '/api/progreso/<id>/eliminar/'
            }
        },
        'documentation': 'Consulta la documentación en /admin/ para más detalles'
    })


@csrf_exempt
@require_http_methods(["POST"])
def vista_inicio_sesion(request):
    """
    API para el inicio de sesión de usuarios
    """
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return JsonResponse({
                'success': False,
                'message': 'Username y password son requeridos'
            }, status=400)
        
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({
                'success': True,
                'message': f'¡Bienvenido, {user.first_name or user.username}!',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'is_active': user.is_active,
                    'date_joined': user.date_joined.isoformat()
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Credenciales inválidas'
            }, status=401)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'JSON inválido'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error interno: {str(e)}'
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def vista_cerrar_sesion(request):
    """
    API para cerrar sesión
    """
    try:
        logout(request)
        return JsonResponse({
            'success': True,
            'message': 'Has cerrado sesión correctamente'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al cerrar sesión: {str(e)}'
        }, status=500)


@login_required
def vista_dashboard(request):
    """
    API del dashboard después del inicio de sesión
    """
    try:
        # Obtener perfil
        try:
            perfil = request.user.perfil
        except PerfilUsuario.DoesNotExist:
            perfil = PerfilUsuario.objects.create(usuario=request.user)
        
        # Obtener usuario personalizado
        try:
            usuario = Usuario.objects.get(correo=request.user.email)
            nombre_completo = usuario.nombre
        except Usuario.DoesNotExist:
            nombre_completo = f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username
        
        # Preparar datos de perfil
        perfil_data = {
            'first_name': perfil.first_name or request.user.first_name or '',
            'last_name': perfil.last_name or request.user.last_name or '',
            'telefono': perfil.telefono or '',
            'fecha_nacimiento': perfil.fecha_nacimiento.isoformat() if perfil.fecha_nacimiento else None,
            'direccion': perfil.direccion or '',
            'avatar': perfil.avatar.url if perfil.avatar else None,
            'fecha_creacion': perfil.fecha_creacion.isoformat(),
            'fecha_actualizacion': perfil.fecha_actualizacion.isoformat()
        }

        user_data = {
            'id': request.user.id,
            'username': request.user.username,
            'email': request.user.email,
            'first_name': request.user.first_name or '',
            'last_name': request.user.last_name or '',
            'nombre_completo': nombre_completo,
            'is_active': request.user.is_active,
            'date_joined': request.user.date_joined.isoformat()
        }

        return JsonResponse({
            'success': True,
            'user': user_data,
            'perfil': perfil_data
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al obtener datos del dashboard: {str(e)}'
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def vista_registro(request):
    """
    API para el registro de usuarios
    """
    try:
        data = json.loads(request.body)
        
        # Validar campos requeridos
        required_fields = ['email', 'password', 'username']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({
                    'success': False,
                    'message': f'El campo {field} es requerido'
                }, status=400)
        
        # Verificar que el email no exista
        if User.objects.filter(email=data['email']).exists():
            return JsonResponse({
                'success': False,
                'message': 'El email ya está registrado'
            }, status=400)
        
        # Verificar que el username no exista
        if User.objects.filter(username=data['username']).exists():
            return JsonResponse({
                'success': False,
                'message': 'El nombre de usuario ya está registrado'
            }, status=400)
        
        # Crear el usuario de Django con nombre y apellido opcionales
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        
        # Actualizar first_name y last_name si se proporcionan
        user.first_name = data.get('first_name', '')
        user.last_name = data.get('last_name', '')
        user.save()
        
        # Crear el usuario personalizado
        nombre_completo = f"{data.get('first_name', '')} {data.get('last_name', '')}".strip()
        if not nombre_completo:
            nombre_completo = data['username']
            
        usuario = Usuario.objects.create(
            nombre=nombre_completo,
            correo=data['email'],
            contrasena=data['password']  # Nota: en producción deberías encriptar esta contraseña
        )
        
        return JsonResponse({
            'success': True,
            'message': '¡Cuenta creada exitosamente! Ahora puedes iniciar sesión.',
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'nombre_completo': usuario.nombre
            }
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'JSON inválido'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al crear usuario: {str(e)}'
        }, status=500)


@csrf_exempt
@login_required
def vista_perfil(request):
    """
    API para ver y editar el perfil del usuario
    """
    try:
        # Obtener o crear perfil
        try:
            perfil = request.user.perfil
        except PerfilUsuario.DoesNotExist:
            perfil = PerfilUsuario.objects.create(usuario=request.user)
        
        if request.method == 'GET':
            # Obtener usuario personalizado
            try:
                usuario = Usuario.objects.get(correo=request.user.email)
                nombre_completo = usuario.nombre
            except Usuario.DoesNotExist:
                nombre_completo = f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username

            # Preparar datos de usuario y perfil
            user_data = {
                'id': request.user.id,
                'username': request.user.username,
                'email': request.user.email,
                'first_name': request.user.first_name or '',
                'last_name': request.user.last_name or '',
                'nombre_completo': nombre_completo
            }
            
            perfil_data = {
                'first_name': perfil.first_name or request.user.first_name or '',
                'last_name': perfil.last_name or request.user.last_name or '',
                'telefono': perfil.telefono or '',
                'fecha_nacimiento': perfil.fecha_nacimiento.isoformat() if perfil.fecha_nacimiento else None,
                'direccion': perfil.direccion or '',
                'avatar': perfil.avatar.url if perfil.avatar else None,
                'fecha_creacion': perfil.fecha_creacion.isoformat(),
                'fecha_actualizacion': perfil.fecha_actualizacion.isoformat()
            }
            
            return JsonResponse({
                'success': True,
                'user': user_data,
                'perfil': perfil_data
            })
        
        elif request.method == 'POST':
            try:
                data = json.loads(request.body)
                
                # Actualizar datos del perfil
                perfil.telefono = data.get('telefono', perfil.telefono)
                perfil.direccion = data.get('direccion', perfil.direccion)
                
                # Manejar fecha de nacimiento
                fecha_nacimiento = data.get('fecha_nacimiento')
                if fecha_nacimiento:
                    from datetime import datetime
                    try:
                        perfil.fecha_nacimiento = datetime.fromisoformat(fecha_nacimiento).date()
                    except ValueError:
                        return JsonResponse({
                            'success': False,
                            'message': 'Formato de fecha inválido. Use YYYY-MM-DD'
                        }, status=400)
                
                # Actualizar datos del usuario y perfil
                if 'first_name' in data:
                    perfil.first_name = data['first_name']
                    request.user.first_name = data['first_name']
                if 'last_name' in data:
                    perfil.last_name = data['last_name']
                    request.user.last_name = data['last_name']
                
                # Actualizar el usuario personalizado si existe
                try:
                    usuario = Usuario.objects.get(correo=request.user.email)
                    if 'first_name' in data or 'last_name' in data:
                        usuario.nombre = f"{request.user.first_name} {request.user.last_name}"
                        usuario.save()
                except Usuario.DoesNotExist:
                    pass
                
                request.user.save()
                perfil.save()

            except json.JSONDecodeError:
                return JsonResponse({
                    'success': False,
                    'message': 'JSON inválido'
                }, status=400)
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'message': f'Error al actualizar perfil: {str(e)}'
                }, status=500)
            
            try:
                usuario = Usuario.objects.get(correo=request.user.email)
                nombre_completo = usuario.nombre
            except Usuario.DoesNotExist:
                nombre_completo = f"{request.user.first_name} {request.user.last_name}"

            return JsonResponse({
                'success': True,
                'message': 'Perfil actualizado correctamente',
                'user': {
                    'id': request.user.id,
                    'username': request.user.username,
                    'email': request.user.email,
                    'first_name': request.user.first_name,
                    'last_name': request.user.last_name,
                    'nombre_completo': nombre_completo
                },
                'perfil': {
                    'telefono': perfil.telefono,
                    'fecha_nacimiento': perfil.fecha_nacimiento.isoformat() if perfil.fecha_nacimiento else None,
                    'direccion': perfil.direccion,
                    'avatar': perfil.avatar.url if perfil.avatar else None,
                    'fecha_creacion': perfil.fecha_creacion.isoformat(),
                    'fecha_actualizacion': perfil.fecha_actualizacion.isoformat()
                }
            })
        
        else:
            return JsonResponse({
                'success': False,
                'message': 'Método no permitido'
            }, status=405)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'JSON inválido'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al procesar perfil: {str(e)}'
        }, status=500)
