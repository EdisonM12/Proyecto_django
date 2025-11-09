from django.shortcuts import render
from .models import Curso, Profesor
from .forms import CursoForm, ProfesorForm
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
#def login(request):
    #return render(request, 'app/login.html')

def login(request):
    return render(request, 'curso/home_curso.html')

def crear_curso(request):
    form = CursoForm()

    if request.method == "POST":
        form = CursoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('app:listar_cursos')

    return render(request, 'curso/crear_curso.html', {'form': form})

def listar_cursos(request):
    cursos = Curso.objects.all()
    return render(request, "curso/listar_cursos.html", {"cursos": cursos})

def editar_curso(request, id):
    curso = get_object_or_404(Curso, id=id)
    form = CursoForm(request.POST or None, instance=curso)

    if form.is_valid():
        form.save()
        return redirect("app:listar_cursos")

    return render(request, "curso/editar_curso.html", {
        "form": form,
        "curso": curso
    })
def eliminar_curso(request, id):
    cursos = get_object_or_404(Curso, id=id)

    if request.method == "POST":
        cursos.delete()
        return redirect("app:listar_cursos")

    return render(request, "curso/eliminar_curso.html", {
        "curso": cursos
    })
#profesor

def listar_profesor(request):
    profesores = Profesor.objects.all()
    return render(request, "curso/listar_profesor.html", {"profesores": profesores})
def crear_profesor(request):
    form = ProfesorForm()

    if request.method == "POST":
        form = ProfesorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('app:listar_profesor')

    return render(request, 'curso/crear_profesor.html', {'form': form})
def editar_profesor(request, id):
    profesor = get_object_or_404(Profesor, id=id)
    form = ProfesorForm(request.POST or None, instance=profesor)

    if form.is_valid():
        form.save()
        return redirect("app:listar_profesor")

    return render(request, "curso/editar_profesor.html", {
        "form": form,
        "profesor": profesor
    })
def eliminar_profesor(request, id):
    profesor = get_object_or_404(Profesor, id=id)

    if request.method == "POST":
        profesor.delete()
        return redirect("app:listar_profesor")

    return render(request, "curso/eliminar_profesor.html", {
        "profesor": profesor
    })