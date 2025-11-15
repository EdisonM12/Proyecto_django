from django.shortcuts import render, redirect, get_object_or_404
from .models import Estudiante,Evaluaciones, Profesor, Curso, Calificacion, Materia
from .forms import Login1, EstudianteForm, EvaluacionesForm, ProfesorForm, CursoForm, CalificacionForm, MateriaForm


# LOGIN
def home(request):

    return render(request, "app/Inicio.html")

def pag_profesor(request):

    return render(request, "profesor/index_profesor.html")

def Login_Admin(request):
    form = Login1()
    if request.method == "POST":
        form = Login1(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data['email']
            password = form.cleaned_data['password']
            return redirect("app:inicio")

    return render(request, "app/login.html", {"form" : form })

#def home_page(request):
    #return render(request, "app/Home_admin.html")
def home_page(request):
    profesores = Profesor.objects.all()  # Trae todos los profesores
    return render(request, "app/Home_admin.html", {"profesores": profesores})



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


# Create your views here.
#def login(request):
    #return render(request, 'app/login.html')

#def login(request):
   # return render(request, 'curso/home_curso.html')

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

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Profesor
from .forms import ProfesorForm

# LISTAR PROFESORES
def listar_profesor(request):
    profesores = Profesor.objects.all()
    context = {
        "profesores": profesores,
        "mostrar_crear": True,
        "mostrar_editar": True,
        "mostrar_eliminar": True,
    }
    return render(request, "curso/listar_profesor.html", context)


# CREAR PROFESOR
def crear_profesor(request):
    form = ProfesorForm()
    if request.method == "POST":
        form = ProfesorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('app:inicio')

    context = {
        "form": form,
        "accion": "Crear",
        "mostrar_crear": False,
        "mostrar_editar": False,
        "mostrar_eliminar": False,
    }
    return render(request, 'curso/crear_profesor.html', context)


# EDITAR PROFESOR
def editar_profesor(request, id):
    profesor = get_object_or_404(Profesor, id=id)
    form = ProfesorForm(request.POST or None, instance=profesor)
    if form.is_valid():
        form.save()
        return redirect("app:inicio")

    context = {
        "form": form,
        "profesor": profesor,
        "accion": "Editar",
        "mostrar_crear": False,
        "mostrar_editar": True,  # Solo mostrar el botón de editar
        "mostrar_eliminar": False,
    }
    return render(request, "curso/editar_profesor.html", context)


# ELIMINAR PROFESOR
def eliminar_profesor(request, id):
    profesor = get_object_or_404(Profesor, id=id)
    if request.method == "POST":
        profesor.delete()
        return redirect("app:inicio")

    context = {
        "profesor": profesor,
        "mostrar_crear": False,
        "mostrar_editar": False,
        "mostrar_eliminar": True,  # Solo mostrar eliminar
    }
    return render(request, "curso/eliminar_profesor.html", context)

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


#CRUD DE MATERIAS

# LISTAR todas las materias
def lista_materias(request):
    materias = Materia.objects.all()
    return render(request, 'app/materia_list.html', {'materias': materias})

# CREAR una nueva materia
def crear_materia(request):
    if request.method == 'POST':
        form = MateriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_materias')
    else:
        form = MateriaForm()
    return render(request, 'app/materia_form.html', {'form': form, 'accion': 'Crear'})

# EDITAR una materia existente
def editar_materia(request, pk):
    materia = get_object_or_404(Materia, pk=pk)
    if request.method == 'POST':
        form = MateriaForm(request.POST, instance=materia)
        if form.is_valid():
            form.save()
            return redirect('lista_materias')
    else:
        form = MateriaForm(instance=materia)
    return render(request, 'app/materia_form.html', {'form': form, 'accion': 'Editar'})

# ELIMINAR una materia
def eliminar_materia(request, pk):
    materia = get_object_or_404(Materia, pk=pk)
    if request.method == 'POST':
        materia.delete()
        return redirect('lista_materias')
    return render(request, 'app/delete_materia.html', {'materia': materia})
