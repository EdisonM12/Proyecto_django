from django.test import TestCase
from django.urls import reverse
from app.models import Estudiantes_pendientes

class RegistrarEstudianteTest(TestCase):

    def test_registrar_estudiante(self):
        """Prueba que el registro crea un estudiante y hace redirect"""

        data = {
            'nombre': 'Edison',
            'apellido': 'Matute',
            'direccion': 'Guayaquil',
            'telefono': '0987654321',
            'cedula': '1234567890',
            'email': 'edison@test.com',
            'password': '12345'
        }

        response = self.client.post(reverse('app:registrar_estudiante'), data)

        # 1. Se crea el objeto
        self.assertEqual(Estudiantes_pendientes.objects.count(), 1)

        estudiante = Estudiantes_pendientes.objects.first()
        self.assertEqual(estudiante.nombre, 'Edison')

        # 2. Hace redirect
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("app:Estudiante_login"))
