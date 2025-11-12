from django.shortcuts import render, redirect, get_object_or_404
from .forms import Login1, EstudianteForm, EvaluacionesForm
from .models import Estudiante, Evaluaciones

# LOGIN
def home(request):
    form = Login1(request.POST or None)
    if request.method == "POST" and form.is_valid():
        return redirect("home1")  # redirige al CRUD
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





#EVALUACIONES
#CREAR EVALIUACIONES
def list_evaluacion(request):
    evalua = Evaluaciones.objects.all()
    return render(request, "eval/list_eva.html", {"evaluaciones": evalua})

def crear_evaluaciones(request):
    if request.method == "POST":
        form = EvaluacionesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("evaluaciones_tabla")
    else:
        form = EvaluacionesForm()
    return render(request, "eval/evaluaciones_form.html", {"form": form, "accion": "Crear"})

def actualizar_Evaluacion(request, id):
    evaluar1 = get_object_or_404(Evaluaciones, id=id)
    if request.method == "POST":
        form = EvaluacionesForm(request.POST, request.FILES, instance=evaluar1)
        if form.is_valid():
            form.save()
            return redirect("evaluaciones_tabla")
    else:
        form = EvaluacionesForm(instance=evaluar1)
    return render(request, "eval/evaluaciones_form.html", {"form": form, "accion": "Editar"})

def eliminar_evalu(request, id):
    eval = get_object_or_404(Evaluaciones, id=id)
    if request.method == "POST":
        eval.delete()
        return redirect("estudiantes_tabla")
    return render(request, "eval/deletefo.html", {"estudiante": eval})

def home1(request):
    return render(request, "app/Home_admin.html")

