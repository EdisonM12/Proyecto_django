from django.forms import ValidationError


class Validaciones:
    def __init__(self, correo):
        self.correo = correo

    def __call__(self, value):
        correo = value.correo
