from django.urls import path
from . import views
app_name = "app"
urlpatterns = [
    path('', views.home, name='home'),  # página de login
    path('estudiantes/', views.listar_estudiantes, name='listar_estudiantes'),  # lista de estudiantes
    path('estudiante/nuevo/', views.crear_estudiante, name='crear_estudiante'),  # crear estudiante
    path('estudiante/<int:id>/editar/', views.actualizar_estudiante, name='actualizar_estudiante'),  # editar estudiante
    path('estudiante/<int:id>/eliminar/', views.eliminar_estudiante, name='eliminar_estudiante'),

    path('evaluacione/', views.list_evaluacion, name= 'evaluaciones_tabla' ), # eliminar estudiante
    path('evaluaciones/nuevo/', views.crear_evaluaciones, name='crear_evaluaciones'),  # crear estudiante
    path('evaluaciones/<int:id>/editar/', views.actualizar_Evaluacion, name='actualizar_evaluaciones'),  # editar estudiante
    path('evaluaciones/<int:id>/eliminar/', views.eliminar_evalu, name='eliminar_evaluaciones'),
    path("listar_calificaciones/", views.listar_calificaciones, name="listar_calificaciones"),
    path("crear_calificacion/", views.crear_calificacion, name="crear_calificacion"),
    path("editar_calificacion/<int:id>/", views.editar_calificacion, name="editar_calificacion"),
    path("eliminar_calificacion/<int:id>/", views.eliminar_calificacion, name="eliminar_calificacion"),
]

