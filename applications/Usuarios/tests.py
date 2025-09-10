from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import PerfilUsuario


class InicioSesionTestCase(TestCase):
    """
    Casos de prueba para la aplicación de inicio de sesión
    """
    
    def setUp(self):
        """
        Configuración inicial para las pruebas
        """
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.perfil = PerfilUsuario.objects.create(
            usuario=self.user,
            telefono='+1234567890',
            direccion='Test Address'
        )
    
    def test_inicio_sesion_exitoso(self):
        """
        Prueba el inicio de sesión exitoso
        """
        response = self.client.post(reverse('inicio_sesion:inicio_sesion'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirección después del login
    
    def test_inicio_sesion_fallido(self):
        """
        Prueba el inicio de sesión con credenciales incorrectas
        """
        response = self.client.post(reverse('inicio_sesion:inicio_sesion'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)  # Página de login
        self.assertContains(response, 'Credenciales inválidas')
    
    def test_cerrar_sesion(self):
        """
        Prueba el cierre de sesión
        """
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('inicio_sesion:cerrar_sesion'))
        self.assertEqual(response.status_code, 302)  # Redirección después del logout
    
    def test_dashboard_requiere_login(self):
        """
        Prueba que el dashboard requiere autenticación
        """
        response = self.client.get(reverse('inicio_sesion:dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirección al login
    
    def test_dashboard_con_login(self):
        """
        Prueba el acceso al dashboard con usuario autenticado
        """
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('inicio_sesion:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')
    
    def test_creacion_perfil_automatica(self):
        """
        Prueba que se crea un perfil automáticamente si no existe
        """
        # Crear un usuario sin perfil
        user_sin_perfil = User.objects.create_user(
            username='nuevouser',
            password='testpass123'
        )
        
        self.client.login(username='nuevouser', password='testpass123')
        response = self.client.get(reverse('inicio_sesion:perfil'))
        self.assertEqual(response.status_code, 200)
        
        # Verificar que se creó el perfil
        self.assertTrue(PerfilUsuario.objects.filter(usuario=user_sin_perfil).exists())
