from django.shortcuts import render, redirect, get_object_or_404
from .forms import Login1, EstudianteForm, EvaluacionesForm, CalificacionForm
from .models import Estudiante, Evaluaciones, Calificacion

# LOGIN
#def home(request):
 #   form = Login1(request.POST or None)
  #  if request.method == "POST" and form.is_valid():
   #     return redirect("evaluaciones_tabla")  # redirige al CRUD
    #return render(request, "app/login.html", {"form": form})
#def home(request):
 #   form = Login1(request.POST or None)
  #  if request.method == "POST" and form.is_valid():
   #     return redirect("evaluaciones_tabla")  # redirige al CRUD
    #return render(request, "app/login.html", {"form": form})

def home(request):

    return render(request, "profesor/index_profesor.html")


# CREAR ESTUDIANTE
def crear_estudiante(request):
    if request.method == "POST":
        form = EstudianteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("app:listar_estudiantes")
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
            return redirect("app:listar_estudiantes")
    else:
        form = EstudianteForm(instance=estudiante)
    return render(request, "app/estudiante_form.html", {"form": form, "accion": "Editar"})


# ELIMINAR ESTUDIANTE
def eliminar_estudiante(request, id):
    estudiante = get_object_or_404(Estudiante, id=id)
    if request.method == "POST":
        estudiante.delete()
        return redirect("app:listar_estudiantes")
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
            return redirect("app:evaluaciones_tabla")
    else:
        form = EvaluacionesForm()
    return render(request, "eval/evaluaciones_form.html", {"form": form, "accion": "Crear"})

def actualizar_Evaluacion(request, id):
    evaluar1 = get_object_or_404(Evaluaciones, id=id)
    if request.method == "POST":
        form = EvaluacionesForm(request.POST, request.FILES, instance=evaluar1)
        if form.is_valid():
            form.save()
            return redirect("app:evaluaciones_tabla")
    else:
        form = EvaluacionesForm(instance=evaluar1)
    return render(request, "eval/evaluaciones_form.html", {"form": form, "accion": "Editar"})

def eliminar_evalu(request, id):
    eval = get_object_or_404(Evaluaciones, id=id)
    if request.method == "POST":
        eval.delete()
        return redirect("app:evaluaciones_tabla")
    return render(request, "eval/deletefo.html", {"estudiante": eval})

def listar_calificaciones(request):
    calificaciones = Calificacion.objects.all()
    return render(request, "calificacion/listar_calificaciones.html", {
        "calificaciones": calificaciones
    })


def crear_calificacion(request):
    form = CalificacionForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("app:listar_calificaciones")
    return render(request, "calificacion/crear_calificacion.html", {"form": form})


def editar_calificacion(request, id):
    calificacion = get_object_or_404(Calificacion, id=id)
    form = CalificacionForm(request.POST or None, instance=calificacion)
    if form.is_valid():
        form.save()
        return redirect("app:listar_calificaciones")
    return render(request, "calificacion/editar_calificacion.html", {"form": form})


def eliminar_calificacion(request, id):
    calificacion = get_object_or_404(Calificacion, id=id)
    if request.method == "POST":
        calificacion.delete()
        return redirect("app:listar_calificaciones")
    return render(request, "calificacion/eliminar_calificacion.html", {
        "calificacion": calificacion
    })