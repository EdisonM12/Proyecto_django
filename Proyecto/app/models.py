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
    telefono = models.CharField(unique=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Evaluaciones(models.Model):
    materia = models.CharField(max_length=255)
    periodo = models.CharField(max_length=255)
    pendiente = models.BooleanField()
    archivo = models.FileField(upload_to='pdfs/', null=True, blank=True)

    def __str__(self):
        return f"{self.materia} - {self.periodo}"


class Calificacion(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name="calificaciones")
    evaluacion = models.ForeignKey(Evaluaciones, on_delete=models.CASCADE, related_name="calificaciones")
    nota = models.DecimalField(max_digits=4, decimal_places=2)
    fecha_registro = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ("estudiante", "evaluacion")

    def __str__(self):
        return f"{self.estudiante} - {self.evaluacion} = {self.nota}"


