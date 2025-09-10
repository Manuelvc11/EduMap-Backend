from django.db import models
from django.contrib.auth.models import User


class ProgresoUsuario(models.Model):
    """Modelo para almacenar el progreso de los usuarios en diferentes actividades"""
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario")
    actividad = models.CharField(max_length=100, verbose_name="Actividad")
    progreso = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, verbose_name="Progreso (%)")
    fecha_inicio = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Inicio")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")
    completado = models.BooleanField(default=False, verbose_name="Completado")
    resultado = models.TextField(blank=True, null=True, verbose_name="Resultado")
    
    class Meta:
        verbose_name = "Progreso de Usuario"
        verbose_name_plural = "Progresos de Usuarios"
        unique_together = ['usuario', 'actividad']
        ordering = ['-fecha_actualizacion']
    
    def __str__(self):
        return f"{self.usuario.username} - {self.actividad} ({self.progreso}%)"


class LogProgreso(models.Model):
    """Modelo para registrar el historial de cambios en el progreso"""
    
    progreso_usuario = models.ForeignKey(ProgresoUsuario, on_delete=models.CASCADE, related_name='logs')
    progreso_anterior = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Progreso Anterior")
    progreso_nuevo = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Progreso Nuevo")
    fecha_cambio = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Cambio")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción del Cambio")
    
    class Meta:
        verbose_name = "Log de Progreso"
        verbose_name_plural = "Logs de Progreso"
        ordering = ['-fecha_cambio']
    
    def __str__(self):
        return f"Log {self.progreso_usuario} - {self.fecha_cambio}"
