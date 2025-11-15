from django import forms
from .models import Curso, Profesor, Administrador, Estudiante, Evaluaciones, Calificacion
import re
from datetime import date

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ["codigo","nombre","descripcion","profesor"]

    def clean(self):
        cleaned = super().clean()
        codigo = cleaned.get("codigo")
        nombre = cleaned.get("nombre")

        if codigo and nombre:
            if codigo.lower() == nombre.lower():
                raise forms.ValidationError("El código no puede ser igual al nombre del curso.")

        return cleaned

    def clean_codigo(self):
        codigo = self.cleaned_data["codigo"].strip()
        if len(codigo) == 0:
            raise forms.ValidationError("Este campo no puede estar vacío")
        if len(codigo) < 3:
            raise forms.ValidationError("El código debe tener al menos 3 dígitos ")
        if len(codigo) > 8:
            raise forms.ValidationError("El código no puede tener más de 8 dígitos")
        if not re.match(r'^[A-Za-z0-9\-]+$', codigo):
            raise forms.ValidationError("El código solo puede contener letras, números y guiones.")
        qs = Curso.objects.filter(codigo__iexact=codigo)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Este código ya está registrado en otro curso.")

        return codigo


    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"].strip()
        if len(nombre) == 0:
            raise forms.ValidationError("Este campo no puede estar vacío")
        if nombre.isdigit():
            raise forms.ValidationError("El nombre no puede ser solo números")
        return nombre

    def clean_descripcion(self):
        descripcion = self.cleaned_data["descripcion"].strip()
        if descripcion and len(descripcion) < 10:
            raise forms.ValidationError("La descripción debe ser más específica")
        return descripcion

class ProfesorForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(
        input_formats=['%d/%m/%Y'],  # día/mes/año
        widget=forms.DateInput(format='%d/%m/%Y')
    )
    class Meta:
        model = Profesor
        fields = ["nombre","apellido","cedula","correo","fecha_nacimiento", "materia"]
    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"].strip()
        if len(nombre) == 0:
            raise forms.ValidationError("Este campo no puede estar vacío")
        if nombre.isdigit():
            raise forms.ValidationError("El nombre no puede ser solo números")
        return nombre
    def clean_apellido(self):
        apellido = self.cleaned_data["apellido"].strip()
        if len(apellido) == 0:
            raise forms.ValidationError("Este campo no puede estar vacío")
        if apellido.isdigit():
            raise forms.ValidationError("El nombre no puede ser solo números")
        return apellido

    def clean_cedula(self):
        cedula = self.cleaned_data.get('cedula')


        if len(cedula) != 10:
            raise forms.ValidationError("La cédula debe tener exactamente 10 dígitos.")


        if not cedula.isdigit():
            raise forms.ValidationError("La cédula debe contener solo números.")


        coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2]
        total = 0
        for i in range(9):
            val = int(cedula[i]) * coeficientes[i]
            if val >= 10:
                val -= 9
            total += val
        modulo = total % 10
        verificador = 0 if modulo == 0 else 10 - modulo
        if verificador != int(cedula[9]):
            raise forms.ValidationError("Cédula inválida.")


        qs = Profesor.objects.filter(cedula=cedula)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Esta cédula ya está registrada.")

        return cedula

    def clean_correo(self):
        correo = self.cleaned_data.get('correo')
        if not correo or len(correo.strip()) == 0:
            raise forms.ValidationError("El correo no puede estar vacío")
        if "@" not in correo:
            raise forms.ValidationError("El correo debe contener '@'")
        if "." not in correo:
            raise forms.ValidationError("El correo debe contener un dominio válido (ejemplo: .com)")

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("Este correo ya está registrado")

        return correo

    def clean_fecha_nacimiento(self):
        fecha = self.cleaned_data.get('fecha_nacimiento')
        if not fecha:
            raise forms.ValidationError("Debes ingresar una fecha de nacimiento.")

        hoy = date.today()

        if fecha > hoy:
            raise forms.ValidationError("La fecha de nacimiento no puede ser futura.")


        edad = hoy.year - fecha.year - ((hoy.month, hoy.day) < (fecha.month, fecha.day))
        if edad < 18:
            raise forms.ValidationError("El estudiante debe tener al menos 5 años.")
        if edad > 80:
            raise forms.ValidationError("Edad no válida.")

        return fecha

    def clean_materia(self):
        materia = self.cleaned_data.get('materia')
        if not materia:
            raise forms.ValidationError("El campo materia no puede estar vacío.")
        return materia
    #************************************************

class Login1(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'input-group input', 'placeholder': 'Correo electrónico'})
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input-group input', 'placeholder': 'Contraseña'})
    )

    def clean(self):
        cleaned = super().clean()
        email = cleaned.get("email")
        password = cleaned.get("password")

         # Validar si existe un admin con ese email y contraseña
        if not Administrador.objects.filter(email=email, password=password).exists():
            raise forms.ValidationError("Correo o contraseña incorrectos")

        return cleaned

class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ['nombre', 'apellido', 'correo', 'direccion', 'telefono']

    def clean_correo(self):
        correo = self.cleaned_data.get("correo")
        qs = Estudiante.objects.filter(correo=correo)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Este correo ya está registrado.")
        return correo

        def clean_telefono(self):
            telefono = str(self.cleaned_data.get("telefono"))

            if not telefono.isdigit():
                raise forms.ValidationError("El teléfono debe tener solo números.")
            if len(telefono) != 10:
                raise forms.ValidationError("El teléfono debe tener exactamente 10 dígitos.")

            qs = Estudiante.objects.filter(telefono=telefono)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("Este teléfono ya está registrado.")

            return telefono

class EvaluacionesForm(forms.ModelForm):
    class Meta:
        model = Evaluaciones
        fields = ['materia', 'periodo', 'pendiente', 'archivo']

    def clean_materia(self):
        materia = self.cleaned_data.get("materia")

        if not materia or materia.strip() == "":
            raise forms.ValidationError("La materia no puede estar vacía.")

        if len(materia) < 3:
            raise forms.ValidationError("La materia debe tener al menos 3 caracteres.")

        return materia

    def clean_periodo(self):
        periodo = self.cleaned_data.get("periodo")

        if not periodo or periodo.strip() == "":
            raise forms.ValidationError("El periodo no puede estar vacío.")

        return periodo

    def clean_archivo(self):
        archivo = self.cleaned_data.get("archivo")

        if archivo:
            if not archivo.name.lower().endswith(".pdf"):
                raise forms.ValidationError("Solo se permiten archivos PDF.")

        return archivo

class CalificacionForm(forms.ModelForm):
    class Meta:
        model = Calificacion
        fields = ['estudiante', 'evaluacion', 'nota']

    def clean_nota(self):
        nota = self.cleaned_data.get("nota")

        if nota is None:
            raise forms.ValidationError("La nota es obligatoria.")

        if nota < 0 or nota > 20:
            raise forms.ValidationError("La nota debe estar entre 0 y 20.")

        return nota

    def clean(self):
        cleaned_data = super().clean()
        estudiante = cleaned_data.get("estudiante")
        evaluacion = cleaned_data.get("evaluacion")

        if estudiante and evaluacion:
            qs = Calificacion.objects.filter(estudiante=estudiante, evaluacion=evaluacion)

            # Ignorar el propio registro si se está editando
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise forms.ValidationError(
                    "Este estudiante ya tiene una calificación para esta evaluación."
                )

        return cleaned_data