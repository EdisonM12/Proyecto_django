from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Estudiante,Evaluaciones, Profesor, Curso, Calificacion, Materia, LoginProfesor, Estudiantes_pendientes, LoginEstudiante
from .forms import Login1, EstudianteForm, EvaluacionesForm, ProfesorForm, CursoForm, CalificacionForm, MateriaForm, Login2, Login3, PendientesForm
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password, check_password


# views.py
def login_estudiante(request):

    if request.method == "POST":
        form_type = request.POST.get('form_type', 'login')

        if form_type == 'registro':

            form_registro = PendientesForm(request.POST, prefix='registro')

            if form_registro.is_valid():
                pendiente = form_registro.save(commit=False)
                pendiente.estado = 'PENDIENTE'
                pendiente.password = make_password(form_registro.cleaned_data['password'])
                pendiente.save()

                return redirect('app:Estudiante_login')

        else:
            # Formulario de LOGIN con prefijo
            form_login = Login3(request.POST, prefix='login')
            if form_login.is_valid():
                email = form_login.cleaned_data['email']
                password = form_login.cleaned_data['password']

                try:
                    usuario = LoginEstudiante.objects.get(email=email)
                    if check_password(password, usuario.password):
                        request.session['estudiante_email'] = email
                        return redirect('app:Estudiante_home')
                    else:
                        form_login.add_error('password', 'Contraseña incorrecta')
                except LoginEstudiante.DoesNotExist:
                    form_login.add_error('email', 'Usuario no encontrado')

    # Crear formularios vacíos CON PREFIJOS
    form_login = Login3(prefix='login')
    form_registro = PendientesForm(prefix='registro')

    return render(request, 'estudiante/estudiante_index.html', {
        'form_login': form_login,
        'form_registro': form_registro
    })


def ver_pendientes(request):
    persona = Estudiantes_pendientes.objects.filter(estado="PENDIENTE")
    return render(request, 'estudiante/pendiente.html', {"pendiente":persona})


def registrar_pendiente(request):
    if request.method == "POST":
        # 1. Crear credenciales

        # 2. Crear pendiente
        Estudiantes_pendientes.objects.create(
            nombre=request.POST['nombre'],
            apellido=request.POST['apellido'],
            direccion=request.POST['direccion'],
            telefono=request.POST['telefono'],
            cedula = request.POST['cedula'],
            email = request.POST['email'],
            password= make_password(request.Post['password']),
            estado = "PENDIENTE"
        )
        messages.success(request, "Registro realizado")

        return redirect("app:Estudiante_login")

    return render(request, "estudiante/estudiante_index.html")



def aceptar_pendiente(request, id):
    pendiente = Estudiantes_pendientes.objects.get(id=id)
    cursos = Curso.objects.all()
    materias = Materia.objects.all()

    if request.method == "POST":
        curso = Curso.objects.get(id=request.POST['curso'])
        materia = Materia.objects.get(id=request.POST['materia'])
        login = LoginEstudiante.objects.create(
            email= pendiente.email,
            password = pendiente.password,
        )

        Estudiante.objects.create(
            nombre=pendiente.nombre,
            apellido=pendiente.apellido,
            direccion=pendiente.direccion,
            telefono=pendiente.telefono,
            cedula = pendiente.cedula,
            curso=curso,
            datos=materia,
            contraseñas=login
        )

        pendiente.delete()
        return redirect("app:listar_estudiantes")
    return render(request, "estudiante/aceptar.html", {
        "pendiente": pendiente,
        "cursos": cursos,
        "materias": materias
    })




def home_estudiante(request):
    return render(request, 'estudiante/home_estudiante.html')
# LOGIN
def cerrar_sesion(request):
    logout(request)
    return redirect('app:home')


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

def Login_profesor(request):
    form = Login2()
    if request.method == "POST":
        form = Login2(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data['email']
            password = form.cleaned_data['password']
            return redirect("app:profesor")

    return render(request, "profesor/login_profesor.html", {"form" : form })

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
            return redirect("app:listar_estudiantes")
    else:
        form = EstudianteForm()
    return render(request, "app/estudiante_form.html", {"form": form, "accion": "Crear"})


# LISTAR ESTUDIANTES
def listar_estudiantes(request):
    estudiantes = Estudiante.objects.all()
    return render(request, "app/listar_estudiantes.html", {
        "estudiantes": estudiantes
    })
def editar_estudiantes(request):
    estudiantes = Estudiante.objects.all()
    return render(request, "app/editar_estudiantes.html", {
        "estudiantes": estudiantes
    })
def editar_estudiantes_detalle(request, id):
    estudiante = get_object_or_404(Estudiante, id=id)
    form = EstudianteForm(request.POST or None, instance=estudiante)

    if form.is_valid():
        form.save()
        return redirect("app:editar_estudiantes")

    return render(request, "app/editar_estudiantes_detalle.html", {
        "form": form,
        "estudiante": estudiante
    })
def eliminar_estudiantes(request):
    estudiantes = Estudiante.objects.all()
    return render(request, "app/eliminar_estudiantes.html", {
        "estudiantes": estudiantes
    })
def eliminar_estudiantes_detalle(request, id):
    estudiante = get_object_or_404(Estudiante, id=id)

    if request.method == "POST":
        estudiante.delete()
        return redirect("app:eliminar_estudiantes")

    return render(request, "app/eliminar_estudiantes_detalle.html", {
        "estudiante": estudiante
    })



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


# LISTAR PROFESORES
def listar_profesores(request):
    profesores = Profesor.objects.all()
    return render(request, "curso/listar_profesor.html", {"profesores": profesores})

# CREAR PROFESOR
def crear_profesor(request):
    form = ProfesorForm()
    if request.method == "POST":
        form = ProfesorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("app:listar_profesor")
    return render(request, "curso/crear_profesor.html", {"form": form})

# EDITAR PROFESOR
def editar_profesor(request):
    profesores = Profesor.objects.all()
    return render(request, "curso/editar_profesor.html", {"profesores": profesores})

def editar_profesor_detalle(request, id):
    profesor = get_object_or_404(Profesor, id=id)
    form = ProfesorForm(request.POST or None, instance=profesor)
    if form.is_valid():
        form.save()
        return redirect("app:editar_profesor")  # vuelve a la lista de edición
    return render(request, "curso/editar_profesor_detalle.html", {"form": form, "profesor": profesor})

# ELIMINAR PROFESOR
def eliminar_profesor(request):
    profesores = Profesor.objects.all()
    return render(request, "curso/eliminar_profesor.html", {"profesores": profesores})
def eliminar_profesor_detalle(request, id):
    profesor = get_object_or_404(Profesor, id=id)
    if request.method == "POST":
        profesor.delete()
        return redirect("app:eliminar_profesor")  # vuelve a la lista de eliminar
    return render(request, "curso/eliminar_profesor_detalle.html", {"profesor": profesor})


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
        return redirect("app:estudiantes_tabla")
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
            return redirect('app:lista_materias')
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
            return redirect('app:lista_materias')
    else:
        form = MateriaForm(instance=materia)
    return render(request, 'app/materia_form.html', {'form': form, 'accion': 'Editar'})

# ELIMINAR una materia
def eliminar_materia(request, pk):
    materia = get_object_or_404(Materia, pk=pk)
    if request.method == 'POST':
        materia.delete()
        return redirect('app:lista_materias')
    return render(request, 'app/delete_materia.html', {'materia': materia})
