from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # página de login
    path('estudiantes/', views.listar_estudiantes, name='estudiantes_tabla'),  # lista de estudiantes
    path('estudiante/nuevo/', views.crear_estudiante, name='crear_estudiante'),  # crear estudiante
    path('estudiante/<int:id>/editar/', views.actualizar_estudiante, name='actualizar_estudiante'),  # editar estudiante
    path('estudiante/<int:id>/eliminar/', views.eliminar_estudiante, name='eliminar_estudiante'),

    path('evaluacione/', views.list_evaluacion, name= 'evaluaciones_tabla' ), # eliminar estudiante
    path('evaluaciones/nuevo/', views.crear_evaluaciones, name='crear_evaluaciones'),  # crear estudiante
    path('evaluaciones/<int:id>/editar/', views.actualizar_Evaluacion, name='actualizar_evaluaciones'),  # editar estudiante
    path('evaluaciones/<int:id>/eliminar/', views.eliminar_evalu, name='eliminar_evaluaciones'),


     path('Home/', views.home1, name='home1'),
]

