from django.db import models

# Create your models here.
class Curso(models.Model):
    codigo= models.CharField(max_length=10, unique=True, default="0001")
    nome= models.CharField(max_length=120)
    nombre = models.CharField(max_length=120)
    descripcion = models.CharField(max_length=120)
    profesor = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

