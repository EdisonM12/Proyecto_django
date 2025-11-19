from django.contrib import messages
from django.core import signing
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Estudiante,Evaluaciones, Profesor, Curso, Calificacion, Materia, LoginProfesor, Estudiantes_pendientes, LoginEstudiante
from .forms import Login1, EstudianteForm, EvaluacionesForm, ProfesorForm, CursoForm, CalificacionForm, MateriaForm, Login2, Login3, PendientesForm
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password, check_password
from .utils.decorador import encrypt, decrypt
from django.core.signing import BadSignature, Signer

def validar_correo(request):
    email = request.GET.get('email')
    existe = Estudiante.objects.filter(email=email).exists() or LoginEstudiante.objects.filter(email=email).exists()
    return JsonResponse({'existe': existe})


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
                messages.success(request, 'El estudiante ha creado correctamente')
                return redirect('app:Estudiante_login')
            else:
                messages.error(request, "corriga los enunciados correspondientes")

        else:

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


    form_login = Login3(prefix='login')
    form_registro = PendientesForm(prefix='registro')

    return render(request, 'estudiante/estudiante_index.html', {
        'form_login': form_login,
        'form_registro': form_registro
    })
def perfil_estudiante(request):
    estudiante_id = request.session.get("estudiante_id")

    if not estudiante_id:
        return redirect("app:Estudiante_login")

    estudiante = Estudiante.objects.get(id=estudiante_id)

    return render(request, "estudiante/perfil.html", {"estudiante": estudiante})

def views_notas(request):
    estudiante_id = request.session.get("estudiante_id")

    if not estudiante_id:
        return redirect("app:Estudiante_login")

    estudiante = Estudiante.objects.get(id=estudiante_id)

    calificaciones = estudiante.calificaciones.select_related(
        "evaluacion__materia"
    )

    return render(request, "estudiante/notas.html", {
        "calificaciones": calificaciones,
        "estudiante": estudiante
    })

def ver_evaluaciones(request):
    estudiante_id = request.session.get("estudiante_id")

    if not estudiante_id:
        return redirect("app:Estudiante_login")

    estudiante = Estudiante.objects.select_related("curso").get(id=estudiante_id)


    evaluaciones = Evaluaciones.objects.filter(curso=estudiante.curso).select_related("materia")

    return render(request, "estudiante/ver_evaluaciones.html", {
        "estudiante": estudiante,
        "evaluaciones": evaluaciones
    })




def ver_pendientes(request):
    persona = Estudiantes_pendientes.objects.filter(estado="PENDIENTE")
    return render(request, 'estudiante/pendiente.html', {"pendiente":persona})


def registrar_pendiente(request):
    if request.method == "POST":



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

    if request.method == "POST":
        curso = Curso.objects.get(id=request.POST['curso'])


        login, creado = LoginEstudiante.objects.get_or_create(
            email=pendiente.email,
            defaults={'password': pendiente.password}
        )



        Estudiante.objects.create(
            nombre=pendiente.nombre,
            apellido=pendiente.apellido,
            direccion=pendiente.direccion,
            telefono=pendiente.telefono,
            cedula=pendiente.cedula,
            curso=curso,
            contraseñas=login
        )

        pendiente.delete()
        return redirect("app:ver_pendiente")

    return render(request, "estudiante/aceptar.html", {
        "pendiente": pendiente,
        "cursos": cursos,
    })




def home_estudiante(request):
    return render(request, 'estudiante/home_estudiante.html')

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


def editar_estudiantes_detalle(request, token):
    try:
        id_real = signing.loads(token)
    except signing.BadSignature:
        return HttpResponse("Token inválido", status=400)

    estudiante = get_object_or_404(Estudiante, id=id_real)
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
def eliminar_estudiantes_detalle(request, token):
    try:
        id_real = signing.loads(token)
    except signing.BadSignature:
        return HttpResponse("Token inválido", status=400)
    estudiante = get_object_or_404(Estudiante, id=id_real)

    if request.method == "POST":
        estudiante.delete()
        return redirect("app:eliminar_estudiantes")

    return render(request, "app/eliminar_estudiantes_detalle.html", {
        "estudiante": estudiante
    })



def crear_curso(request):
    form = CursoForm()

    if request.method == "POST":
        form = CursoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('app:listar_cursos')

    return render(request, 'curso/crear_curso.html', {'form': form})

def listar_cursos(request):
    curso = Curso.objects.all()
    return render(request, "curso/listar_cursos.html", {"curso": curso})

def editar_curso(request):
    curso = Curso.objects.all()
    return render(request, "curso/editar_cursos.html", {
        "curso": curso
    })


def editar_curso_detalle(request, token):
    try:
        id_real = signing.loads(token)
    except signing.BadSignature:
        return HttpResponse("Token inválido", status=400)

    curso = get_object_or_404(Curso, id=id_real)
    form = CursoForm(request.POST or None, instance=curso)

    if form.is_valid():
        form.save()
        return redirect("app:editar_curso")

    return render(request, "curso/editar_curso_detalle.html", {
        "form": form,
        "curso": curso
    })






def eliminar_curso(request):
    curso = Curso.objects.all()
    return render(request, "curso/eliminar_curso.html", {
        "curso": curso
    })
def eliminar_curso_detalle(request, token):
    try:
        id_real = signing.loads(token)
    except signing.BadSignature:
        return HttpResponse("Token inválido", status=400)
    curso = get_object_or_404(Curso, id=id_real)

    if request.method == "POST":
        curso.delete()
        return redirect("app:eliminar_curso")

    return render(request, "curso/eliminar_curso_detalle.html", {
        "curso": curso
    })




def listar_profesores(request):
    profesores = Profesor.objects.all()
    return render(request, "curso/listar_profesor.html", {"profesores": profesores})

def crear_profesor(request):
    form = ProfesorForm()
    if request.method == "POST":
        form = ProfesorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("app:listar_profesores")
    return render(request, "curso/crear_profesor.html", {"form": form})


def editar_profesor(request):
    profesores = Profesor.objects.all()
    return render(request, "curso/editar_profesor.html", {"profesores": profesores})

def editar_profesor_detalle(request, token):
    try:
        id_real = signing.loads(token)
    except signing.BadSignature:
        return HttpResponse("Token inválido", status=400)
    profesor = get_object_or_404(Profesor, id=id_real)
    form = ProfesorForm(request.POST or None, instance=profesor)
    if form.is_valid():
        form.save()
        return redirect("app:editar_profesor")
    return render(request, "curso/editar_profesor_detalle.html", {"form": form, "profesor": profesor})


def eliminar_profesor(request):
    profesores = Profesor.objects.all()
    return render(request, "curso/eliminar_profesor.html", {"profesores": profesores})
def eliminar_profesor_detalle(request, token):
    try:
        id_real = signing.loads(token)
    except signing.BadSignature:
        return HttpResponse("Token inválido", status=400)
    profesor = get_object_or_404(Profesor, id=id_real)
    if request.method == "POST":
        profesor.delete()
        return redirect("app:eliminar_profesor")
    return render(request, "curso/eliminar_profesor_detalle.html", {"profesor": profesor})



def listar_evaluacion(request):
    evalua = Evaluaciones.objects.all()
    return render(request, "eval/listar_evaluacion.html", {"evaluaciones": evalua})

def crear_evaluacion(request):
    if request.method == "POST":
        form = EvaluacionesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("app:crear_evaluacion")
    else:
        form = EvaluacionesForm()
    return render(request, "eval/crear_evaluacion.html", {"form": form, "accion": "Crear"})

def editar_evaluacion(request):
    evaluacion = Evaluaciones.objects.all()
    return render(request, "eval/editar_evaluacion.html", {"evaluacion": evaluacion})

def editar_evaluacion_detalle(request, token):

    try:
        id_real = signing.loads(token)
    except signing.BadSignature:
        return HttpResponse("Token inválido", status=400)
    evaluacion = get_object_or_404(Evaluaciones, id=id_real)
    form = EvaluacionesForm(request.POST or None, instance=evaluacion)
    if form.is_valid():
        form.save()
        return redirect("app:editar_evaluacion")
    return render(request, "eval/editar_evaluacion_detalle.html", {"form": form, "evaluacion": evaluacion})
def eliminar_evaluacion(request):
    evaluacion = Evaluaciones.objects.all()
    return render(request, "eval/eliminar_evaluacion.html", {"evaluacion": evaluacion})
def eliminar_evaluacion_detalle(request, token):
    try:
        id_real = signing.loads(token)
    except signing.BadSignature:
        return HttpResponse("Token inválido", status=400)
    evaluacion = get_object_or_404(Evaluaciones, id=id_real)
    if request.method == "POST":
        evaluacion.delete()
        return redirect("app:eliminar_evaluacion")
    return render(request, "eval/eliminar_evaluacion_detalle.html", {"evaluacion": evaluacion})




def listar_calificacion(request):
    calificacion = Calificacion.objects.all()
    return render(request, "calificacion/listar_calificacion.html", {"calificacion": calificacion})

def crear_calificacion(request):
    if request.method == "POST":
        form = CalificacionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("app:listar_calificacion")
    else:
        form = CalificacionForm()
    return render(request, "calificacion/crear_calificacion.html", {"form": form, "accion": "Crear"})

def editar_calificacion(request):
    calificacion = Calificacion.objects.all()
    return render(request, "calificacion/editar_calificacion.html", {"calificacion": calificacion})


def eliminar_calificacion(request):

    calificacion = Calificacion.objects.all()
    return render(request, "calificacion/eliminar_calificacion.html", {"calificacion": calificacion})
def editar_calificacion_detalle(request, token):
    try:
        id_real = signing.loads(token)
    except signing.BadSignature:
        return HttpResponse("Token inválido", status=400)
    calificacion = get_object_or_404(Calificacion, id=id_real)
    form = CalificacionForm(request.POST or None, instance=calificacion)

    if form.is_valid():
        form.save()
        return redirect("app:editar_calificacion")  # vuelve a la lista de edición

    return render(
        request,
        "calificacion/editar_calificacion_detalle.html",
        {
            "form": form,
            "calificacion": calificacion
        }
    )
def eliminar_calificacion_detalle(request, token):
    try:
        id_real = signing.loads(token)
    except signing.BadSignature:
        return HttpResponse("Token inválido", status=400)
    calificacion = get_object_or_404(Calificacion, id=id_real)
    if request.method == "POST":
        calificacion.delete()
        return redirect("app:eliminar_calificacion")  # vuelve a la lista de eliminar
    return render(request, "calificacion/eliminar_calificacion_detalle.html", {"calificacion": calificacion})





def listar_materia(request):
    materias = Materia.objects.all()
    return render(request, 'app/listar_materia.html', {'materias': materias})

def crear_materia(request):
    if request.method == "POST":
        form = MateriaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("app:crear_materia")
    else:
        form = MateriaForm()
    return render(request, "app/crear_materia.html", {"form": form, "accion": "Crear"})

def editar_materia(request):
    materia = Materia.objects.all()
    return render(request, "app/editar_materia.html", {"materia": materia})


def eliminar_materia(request):

    materia = Materia.objects.all()
    return render(request, "app/eliminar_materia.html", {"materia": materia})
def editar_materia_detalle(request, token):
    try:
        id_real = signing.loads(token)
    except signing.BadSignature:
        return HttpResponse("Token inválido", status=400)
    materia = get_object_or_404(Materia, id=id_real)
    form = MateriaForm(request.POST or None, instance=materia)

    if form.is_valid():
        form.save()
        return redirect("app:editar_materia")

    return render(
        request,
        "app/editar_materia_detalle.html",
        {
            "form": form,
            "materia": materia
        }
    )
def eliminar_materia_detalle(request, token):
    try:
        id_real = signing.loads(token)
    except signing.BadSignature:
        return HttpResponse("Token inválido", status=400)
    materia = get_object_or_404(Materia, id=id_real)
    if request.method == "POST":
        materia.delete()
        return redirect("app:eliminar_materia")
    return render(request, "app/eliminar_materia_detalle.html", {"materia": materia})



