from django.db import models

# Create your models here.
class Profesor(models.Model):
    nombre= models.CharField(max_length=100)
    apellido= models.CharField(max_length=100)
    cedula= models.CharField(max_length=100, unique=True)
    correo= models.EmailField(max_length=100, unique=True)
    fecha_nacimiento= models.DateField()
    materia= models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
class Curso(models.Model):
    codigo= models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=120)
    descripcion = models.CharField(max_length=120)
    profesor = models.ForeignKey(
        Profesor,
        on_delete=models.CASCADE,
        related_name="cursos"
    )

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


