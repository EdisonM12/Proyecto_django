from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = "app"
urlpatterns = [


    path('logout/', views.cerrar_sesion, name='logout'),
    path('login_Estudiante/', views.login_estudiante, name='Estudiante_login'),
    path('profesor/', views.pag_profesor, name='profesor'),
    path("listar_cursos/", views.listar_cursos, name="listar_cursos"),
    path("crear_curso/", views.crear_curso, name="crear_curso"),
    path("editar_curso/<int:id>/", views.editar_curso, name="editar_curso"),
    path("eliminar_curso/<int:id>/", views.eliminar_curso, name="eliminar_curso"),
    path("profesores/", views.listar_profesores, name="listar_profesores"),
    path("profesores/nuevo/", views.crear_profesor, name="crear_profesor"),
    path("profesores/editar/", views.editar_profesor, name="editar_profesor"),
    path("profesores/eliminar/", views.eliminar_profesor, name="eliminar_profesor"),
    path("profesores/<int:id>/editar/", views.editar_profesor_detalle, name="editar_profesor_detalle"),
    path("profesores/<int:id>/eliminar/", views.eliminar_profesor_detalle, name="eliminar_profesor_detalle"),
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
    path("estudiantes/editar/<int:id>/", views.editar_estudiantes_detalle, name="editar_estudiantes_detalle"),


    path("estudiantes/eliminar/", views.eliminar_estudiantes, name="eliminar_estudiantes"),
    path("estudiantes/eliminar/<int:id>/", views.eliminar_estudiantes_detalle, name="eliminar_estudiantes_detalle"),


    path('evaluacione/', views.list_evaluacion, name= 'evaluaciones_tabla' ),
    path('evaluaciones/nuevo/', views.crear_evaluaciones, name='crear_evaluaciones'),
    path('evaluaciones/<int:id>/editar/', views.actualizar_Evaluacion, name='actualizar_evaluaciones'),
    path('evaluaciones/<int:id>/eliminar/', views.eliminar_evalu, name='eliminar_evaluaciones'),

    path("listar_calificaciones/", views.listar_calificaciones, name="listar_calificaciones"),
    path("crear_calificacion/", views.crear_calificacion, name="crear_calificacion"),
    path("editar_calificacion/<int:id>/", views.editar_calificacion, name="editar_calificacion"),
    path("eliminar_calificacion/<int:id>/", views.eliminar_calificacion, name="eliminar_calificacion"),

#MATERIA
    path('materias/', views.lista_materias, name='lista_materias'),
    path('materias/crear/', views.crear_materia, name='crear_materia'),
    path('materias/editar/<int:pk>/', views.editar_materia, name='editar_materia'),
    path('materias/eliminar/<int:pk>/', views.eliminar_materia, name='eliminar_materia'),

]

