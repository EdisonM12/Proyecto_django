from django.shortcuts import render, redirect, get_object_or_404
from .forms import Login1, EstudianteForm
from .models import Estudiante

# LOGIN
def home(request):
    form = Login1(request.POST or None)
    if request.method == "POST" and form.is_valid():
        return redirect("estudiantes_tabla")  # redirige al CRUD
    return render(request, "app/login.html", {"form": form})


# CREAR ESTUDIANTE
def crear_estudiante(request):
    if request.method == "POST":
        form = EstudianteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("estudiantes_tabla")
    else:
        form = EstudianteForm()
    return render(request, "app/estudiante_form.html", {"form": form, "accion": "Crear"})


# LISTAR ESTUDIANTES
def listar_estudiantes(request):
    estudiantes = Estudiante.objects.all()  # <- usar el modelo, no el form
    return render(request, "app/estudiantes_tablas.html", {"estudiantes": estudiantes})


# ACTUALIZAR ESTUDIANTE
def actualizar_estudiante(request, id):
    estudiante = get_object_or_404(Estudiante, id=id)
    if request.method == "POST":
        form = EstudianteForm(request.POST, instance=estudiante)
        if form.is_valid():
            form.save()
            return redirect("estudiantes_tabla")
    else:
        form = EstudianteForm(instance=estudiante)
    return render(request, "app/estudiante_form.html", {"form": form, "accion": "Editar"})


# ELIMINAR ESTUDIANTE
def eliminar_estudiante(request, id):
    estudiante = get_object_or_404(Estudiante, id=id)
    if request.method == "POST":
        estudiante.delete()
        return redirect("estudiantes_tabla")
    return render(request, "app/delete.html", {"estudiante": estudiante})
