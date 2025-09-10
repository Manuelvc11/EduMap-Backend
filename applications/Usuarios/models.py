from django.db import models
from django.contrib.auth.models import User


class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=100)
    

class Progreso(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    leccion = models.CharField(max_length=200)
    categoria = models.CharField(max_length=100)
    fecha_completada = models.DateTimeField(auto_now_add=True)