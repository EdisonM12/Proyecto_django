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

