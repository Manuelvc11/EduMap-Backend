from django.contrib import admin
from .models import ProgresoUsuario, LogProgreso


@admin.register(ProgresoUsuario)
class ProgresoUsuarioAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'actividad', 'progreso', 'completado', 'fecha_actualizacion']
    list_filter = ['completado', 'actividad', 'fecha_inicio', 'fecha_actualizacion']
    search_fields = ['usuario__username', 'usuario__email', 'actividad']
    readonly_fields = ['fecha_inicio', 'fecha_actualizacion']
    list_editable = ['progreso', 'completado']
    ordering = ['-fecha_actualizacion']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('usuario', 'actividad', 'progreso', 'completado')
        }),
        ('Fechas', {
            'fields': ('fecha_inicio', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
        ('Notas', {
            'fields': ('notas',),
            'classes': ('collapse',)
        }),
    )


@admin.register(LogProgreso)
class LogProgresoAdmin(admin.ModelAdmin):
    list_display = ['progreso_usuario', 'progreso_anterior', 'progreso_nuevo', 'fecha_cambio']
    list_filter = ['fecha_cambio', 'progreso_usuario__actividad']
    search_fields = ['progreso_usuario__usuario__username', 'progreso_usuario__actividad', 'descripcion']
    readonly_fields = ['fecha_cambio']
    ordering = ['-fecha_cambio']
    
    def has_add_permission(self, request):
        return False  # Los logs se crean automáticamente
