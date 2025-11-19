from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = "app"
urlpatterns = [


    path('logout/', views.cerrar_sesion, name='logout'),
    path('login_Estudiante/', views.login_estudiante, name='Estudiante_login'),
    path('validar-correo/', views.validar_correo, name='validar_correo'),

    path('profesor/', views.pag_profesor, name='profesor'),
    path("listar_cursos/", views.listar_cursos, name="listar_cursos"),
    path("crear_curso/", views.crear_curso, name="crear_curso"),
    path("editar_curso/<int:id>/", views.editar_curso, name="editar_curso"),
    path("eliminar_curso/<int:id>/", views.eliminar_curso, name="eliminar_curso"),
    path("profesores/", views.listar_profesores, name="listar_profesores"),
    path("profesores/nuevo/", views.crear_profesor, name="crear_profesor"),
    path("profesores/editar/", views.editar_profesor, name="editar_profesor"),
    path("profesores/eliminar/", views.eliminar_profesor, name="eliminar_profesor"),
    path("profesores/<str:token>/editar/", views.editar_profesor_detalle, name="editar_profesor_detalle"),
    path("profesores/<str:token>/eliminar/", views.eliminar_profesor_detalle, name="eliminar_profesor_detalle"),
    path('', views.home, name='home'),  # página de login


    #ADMINISTRADOR LOGIN Y OPCIONES
   path('login/', views.Login_Admin, name='opciones'),
    path('Inicio/', views.home_page, name= 'inicio'),
    path('login_profe/', views.Login_profesor, name='Login_profesor'),
    path('Estudiante_home/', views.home_estudiante, name='Estudiante_home'),



#ACEPTAR SOLI
     path('verPendiente/',views.ver_pendientes, name = "ver_pendiente"),
     path('aceptar//<int:id>/', views.aceptar_pendiente, name = "aceptar_pendiente"),



    path('estudiante/nuevo/', views.crear_estudiante, name='crear_estudiante'),

    path("estudiantes/listar/", views.listar_estudiantes, name="listar_estudiantes"),


    path("estudiantes/editar/", views.editar_estudiantes, name="editar_estudiantes"),
    path("estudiantes/editar/<str:token>/", views.editar_estudiantes_detalle, name="editar_estudiantes_detalle"),


    path("estudiantes/eliminar/", views.eliminar_estudiantes, name="eliminar_estudiantes"),
    path("estudiantes/eliminar/<str:token>/", views.eliminar_estudiantes_detalle, name="eliminar_estudiantes_detalle"),


#evaluaciones
    path('evaluacion/nuevo/', views.crear_evaluacion, name='crear_evaluacion'),

    path("evaluacion/listar/", views.listar_evaluacion, name="listar_evaluacion"),

    path("evaluacion/editar/", views.editar_evaluacion, name="editar_evaluacion"),
    path("evaluacion/editar/<str:token>/", views.editar_evaluacion_detalle, name="editar_evaluacion_detalle"),

    path("evaluacion/eliminar/", views.eliminar_evaluacion, name="eliminar_evaluacion"),
    path("evaluacion/eliminar/<str:token>/", views.eliminar_evaluacion_detalle, name="eliminar_evaluacion_detalle"),

    #path("listar_calificaciones/", views., name="listar_calificaciones"),
   #calificacion
    path('calificacion/nuevo/', views.crear_calificacion, name='crear_calificacion'),

    path("calificacion/listar/", views.listar_calificacion, name="listar_calificacion"),

    path("calificacion/editar/", views.editar_calificacion, name="editar_calificacion"),
    path("calificacion/editar/<str:token>/", views.editar_calificacion_detalle, name="editar_calificacion_detalle"),

    path("calificacion/eliminar/", views.eliminar_calificacion, name="eliminar_calificacion"),
    path("calificacion/eliminar/<str:token>/", views.eliminar_calificacion_detalle, name="eliminar_calificacion_detalle"),
#MATERIA
    path('materia/nuevo/', views.crear_materia, name='crear_materia'),

    path("materia/listar/", views.listar_materia, name="listar_materia"),

    path("materia/editar/", views.editar_materia, name="editar_materia"),
    path("materia/editar/<str:token>/", views.editar_materia_detalle, name="editar_materia_detalle"),

    path("materia/eliminar/", views.eliminar_materia, name="eliminar_materia"),
    path("materia/eliminar/<str:token>/", views.eliminar_materia_detalle, name="eliminar_materia_detalle"),


    #estudiante
    path('perfil/', views.perfil_estudiante, name= 'perfil'),
    path('notas_estudiante/', views.views_notas, name='notas_estudiante'),
    path('ver_evaluaciones/', views.ver_evaluaciones, name = 'evaluaciones_ver')

]


#estudiante
