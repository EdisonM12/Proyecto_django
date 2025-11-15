from django.urls import path
from . import views

app_name = "app"
urlpatterns = [
    #path('', views.login, name='inicio'),
    path("listar_cursos/", views.listar_cursos, name="listar_cursos"),
    path("crear_curso/", views.crear_curso, name="crear_curso"),
    path("editar_curso/<int:id>/", views.editar_curso, name="editar_curso"),
    path("eliminar_curso/<int:id>/", views.eliminar_curso, name="eliminar_curso"),
    path("listar_profesor/", views.listar_profesor, name="listar_profesor"),
    path("crear_profesor/", views.crear_profesor, name="crear_profesor"),
    path("editar_profesor/<int:id>/", views.editar_profesor, name="editar_profesor"),
    path("eliminar_profesor/<int:id>/", views.eliminar_profesor, name="eliminar_profesor"),
    path('', views.home, name='home'),  # página de login
    #ADMINISTRADOR LOGIN Y OPCIONES
   path('login/', views.Login_Admin, name='opciones'),
    path('Inicio/', views.home_page, name= 'inicio'),






    path('estudiantes/', views.listar_estudiantes, name='listar_estudiantes'),
    path('estudiante/nuevo/', views.crear_estudiante, name='crear_estudiante'),
    path('estudiante/<int:id>/editar/', views.actualizar_estudiante, name='actualizar_estudiante'),
    path('estudiante/<int:id>/eliminar/', views.eliminar_estudiante, name='eliminar_estudiante'),

    path('evaluacione/', views.list_evaluacion, name= 'evaluaciones_tabla' ),
    path('evaluaciones/nuevo/', views.crear_evaluaciones, name='crear_evaluaciones'),
    path('evaluaciones/<int:id>/editar/', views.actualizar_Evaluacion, name='actualizar_evaluaciones'),
    path('evaluaciones/<int:id>/eliminar/', views.eliminar_evalu, name='eliminar_evaluaciones'),

    path("listar_calificaciones/", views.listar_calificaciones, name="listar_calificaciones"),
    path("crear_calificacion/", views.crear_calificacion, name="crear_calificacion"),
    path("editar_calificacion/<int:id>/", views.editar_calificacion, name="editar_calificacion"),
    path("eliminar_calificacion/<int:id>/", views.eliminar_calificacion, name="eliminar_calificacion"),
]

