from django.shortcuts import render
from .models import Curso
from .forms import CursoForm
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