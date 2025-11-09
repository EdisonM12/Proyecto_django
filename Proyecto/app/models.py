from django.db import models

# Create your models here.
class Administrador(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    class Meta:
        db_table = "Administrador"
        managed = False

# Estudiante, Evaluación, Calificación

class Estudiante(models.Model):
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    correo = models.EmailField(unique=True)
    direccion = models.CharField(max_length=255)
    telefono = models.IntegerField(unique=True)

class Evaluaciones(models.Model):
    Materia = models.CharField(max_length=255)
    Periodo = models.CharField(max_length=255)
    Pendiente = models.BooleanField()
    archivo = models.FileField(upload_to='pdfs/', null=True, blank=True)  # campo para PDF opcional


