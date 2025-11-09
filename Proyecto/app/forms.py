from django import forms
from .models import Curso
import re

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

    #def clean_profesor(self):
        #profesor = self.cleaned_data["profesor"].strip()
        #if profesor is None:
            #raise forms.ValidationError("Asignar profesor al curso")

