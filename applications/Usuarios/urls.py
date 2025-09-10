from django.urls import path
from . import views

app_name = 'inicio_sesion'

urlpatterns = [
    path('login/', views.vista_inicio_sesion, name='inicio_sesion'),
    path('logout/', views.vista_cerrar_sesion, name='cerrar_sesion'),
    path('register/', views.vista_registro, name='registro'),
    path('dashboard/', views.vista_dashboard, name='dashboard'),
    path('profile/', views.vista_perfil, name='perfil'),
]
