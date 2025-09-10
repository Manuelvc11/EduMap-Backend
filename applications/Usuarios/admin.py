from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import PerfilUsuario


class PerfilUsuarioInline(admin.StackedInline):
    model = PerfilUsuario
    can_delete = False
    verbose_name_plural = 'Perfil'


class UsuarioPersonalizadoAdmin(UserAdmin):
    inlines = (PerfilUsuarioInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')


# Desregistrar el admin por defecto y registrar el personalizado
admin.site.unregister(User)
admin.site.register(User, UsuarioPersonalizadoAdmin)


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'telefono', 'fecha_nacimiento', 'fecha_creacion')
    list_filter = ('fecha_creacion', 'fecha_actualizacion')
    search_fields = ('usuario__username', 'usuario__email', 'telefono')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')
