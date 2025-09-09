from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=100)
    

class Progreso(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    leccion = models.ForeignKey(Leccion, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    fecha_completada = models.DateTimeField(auto_now_add=True)