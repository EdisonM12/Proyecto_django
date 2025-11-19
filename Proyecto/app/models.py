from django.db import models
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password



class Administrador(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    class Meta:
        db_table = "Administrador"
        managed = False



class LoginProfesor(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)




class Profesor(models.Model):
    nombre= models.CharField(max_length=100)
    apellido= models.CharField(max_length=100)
    cedula= models.CharField(max_length=100, unique=True)
    correo= models.EmailField(max_length=100, unique=True)
    fecha_nacimiento= models.DateField(),



    login = models.OneToOneField(LoginProfesor, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
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



class LoginEstudiante(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

class Estudiantes_pendientes(models.Model):
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    email = models.EmailField(unique=True,  null=True , blank=True)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(unique=True, blank= True, null=True )
    cedula = models.CharField(max_length=100, unique=True, null= False, blank=False)
    estado = models.CharField(max_length=20, default="PENDIENTE")
    password = models.CharField(max_length=255, null=True, blank=True)



class Estudiante(models.Model):
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(unique=True, null=True, blank=True)
    cedula = models.CharField(max_length=100, unique=True, null= False, blank=False)
    curso = models.ForeignKey(Curso , on_delete=models.PROTECT, null=True, blank=True)
    contraseñas= models.OneToOneField(LoginEstudiante, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Evaluaciones(models.Model):
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, max_length=255)
    periodo = models.CharField(max_length=255)
    pendiente = models.BooleanField()
    archivo = models.FileField(upload_to='pdfs/', null=True, blank=True)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, null=True, blank=True)

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

