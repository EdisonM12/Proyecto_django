from django import forms
from django.db.models import fields
from .models import Administrador, Estudiante, Evaluaciones,Calificacion

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







