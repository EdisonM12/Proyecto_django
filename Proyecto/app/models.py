from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class Administrador(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    class Meta:
        db_table = "Administrador"
        managed = False

# Estudiante, Evaluación, Calificación




class Profesor(models.Model):
    nombre= models.CharField(max_length=100)
    apellido= models.CharField(max_length=100)
    cedula= models.CharField(max_length=100, unique=True)
    correo= models.EmailField(max_length=100, unique=True)
    fecha_nacimiento= models.DateField()

    def str(self):
        return self.nombre

class Materia(models.Model):
    nombre = models.CharField(max_length=100)
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE, related_name="materias")

    def __str__(self):
        return f"{self.nombre} - {self.profesor.nombre}"




class Curso(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=120)
    descripcion = models.CharField(max_length=120)
    materia = models.ManyToManyField(Materia, related_name='cursos')

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class Estudiante(models.Model):
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    correo = models.EmailField(unique=True)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(unique=True)
    curso = models.ForeignKey(Curso , on_delete=models.PROTECT, null=True, blank=True)

    def _str_(self):
        return f"{self.nombre} {self.apellido}"


class Evaluaciones(models.Model):
    materia = models.CharField(max_length=255)
    periodo = models.CharField(max_length=255)
    pendiente = models.BooleanField()
    archivo = models.FileField(upload_to='pdfs/', null=True, blank=True)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, null=True, blank=True)

    def _str_(self):
        return f"{self.materia} - {self.periodo}"


class Calificacion(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name="calificaciones")
    evaluacion = models.ForeignKey(Evaluaciones, on_delete=models.CASCADE, related_name="calificaciones")
    nota = models.DecimalField(max_digits=4, decimal_places=2)
    fecha_registro = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ("estudiante", "evaluacion")

    def _str_(self):
        return f"{self.estudiante} - {self.evaluacion} = {self.nota}"

