from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # página de login
    path('estudiantes/', views.listar_estudiantes, name='estudiantes_tabla'),  # lista de estudiantes
    path('estudiante/nuevo/', views.crear_estudiante, name='crear_estudiante'),  # crear estudiante
    path('estudiante/<int:id>/editar/', views.actualizar_estudiante, name='actualizar_estudiante'),  # editar estudiante
    path('estudiante/<int:id>/eliminar/', views.eliminar_estudiante, name='eliminar_estudiante'),  # eliminar estudiante
]
