from django.urls import path
from . import views

app_name = 'progreso_usuario'

urlpatterns = [
    path('', views.lista_progreso, name='lista'),
    path('crear/', views.crear_progreso, name='crear'),
    path('<int:pk>/', views.detalle_progreso, name='detalle'),
    path('<int:pk>/editar/', views.editar_progreso, name='editar'),
    path('<int:pk>/eliminar/', views.eliminar_progreso, name='eliminar'),
    path('<int:pk>/actualizar-ajax/', views.actualizar_progreso_ajax, name='actualizar_ajax'),
]
