from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import ProgresoUsuario, LogProgreso


class ProgresoUsuarioModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_crear_progreso_usuario(self):
        """Test para crear un progreso de usuario"""
        progreso = ProgresoUsuario.objects.create(
            usuario=self.user,
            actividad='Aprender Django',
            progreso=50.00
        )
        
        self.assertEqual(progreso.usuario, self.user)
        self.assertEqual(progreso.actividad, 'Aprender Django')
        self.assertEqual(progreso.progreso, 50.00)
        self.assertFalse(progreso.completado)
    
    def test_progreso_completado(self):
        """Test para marcar progreso como completado"""
        progreso = ProgresoUsuario.objects.create(
            usuario=self.user,
            actividad='Aprender Django',
            progreso=100.00,
            completado=True
        )
        
        self.assertTrue(progreso.completado)
    
    def test_unique_together_constraint(self):
        """Test para verificar que no se pueden duplicar usuario-actividad"""
        ProgresoUsuario.objects.create(
            usuario=self.user,
            actividad='Aprender Django',
            progreso=50.00
        )
        
        # Intentar crear otro progreso con el mismo usuario y actividad
        with self.assertRaises(Exception):
            ProgresoUsuario.objects.create(
                usuario=self.user,
                actividad='Aprender Django',
                progreso=75.00
            )


class ProgresoUsuarioViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.progreso = ProgresoUsuario.objects.create(
            usuario=self.user,
            actividad='Aprender Django',
            progreso=50.00
        )
    
    def test_lista_progreso_requiere_login(self):
        """Test que la vista de lista requiere login"""
        response = self.client.get(reverse('progreso_usuario:lista'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_lista_progreso_con_login(self):
        """Test que la vista de lista funciona con login"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('progreso_usuario:lista'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Aprender Django')
    
    def test_detalle_progreso(self):
        """Test para la vista de detalle"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('progreso_usuario:detalle', args=[self.progreso.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Aprender Django')
    
    def test_crear_progreso(self):
        """Test para crear un nuevo progreso"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('progreso_usuario:crear'), {
            'actividad': 'Aprender Python',
            'progreso': 25.00,
            'completado': False,
            'notas': 'Comenzando con lo básico'
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(ProgresoUsuario.objects.filter(actividad='Aprender Python').exists())
    
    def test_actualizar_progreso_ajax(self):
        """Test para actualización AJAX de progreso"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('progreso_usuario:actualizar_ajax', args=[self.progreso.pk]),
            {'progreso': '75.00'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        self.assertEqual(response.status_code, 200)
        self.progreso.refresh_from_db()
        self.assertEqual(self.progreso.progreso, 75.00)


class LogProgresoTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.progreso = ProgresoUsuario.objects.create(
            usuario=self.user,
            actividad='Aprender Django',
            progreso=50.00
        )
    
    def test_crear_log_progreso(self):
        """Test para crear un log de progreso"""
        log = LogProgreso.objects.create(
            progreso_usuario=self.progreso,
            progreso_anterior=50.00,
            progreso_nuevo=75.00,
            descripcion='Progreso actualizado'
        )
        
        self.assertEqual(log.progreso_usuario, self.progreso)
        self.assertEqual(log.progreso_anterior, 50.00)
        self.assertEqual(log.progreso_nuevo, 75.00)
        self.assertEqual(log.descripcion, 'Progreso actualizado')
