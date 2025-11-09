from django import forms
from django.db.models import fields
from .models import Administrador, Estudiante

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








