from django.urls import path
from . import views

app_name = "app"
urlpatterns = [
    path('', views.login, name='inicio'),
    path("listar_cursos/", views.listar_cursos, name="listar_cursos"),
    path("crear_curso/", views.crear_curso, name="crear_curso"),
    path("editar_curso/<int:id>/", views.editar_curso, name="editar_curso"),
    path("eliminar_curso/<int:id>/", views.eliminar_curso, name="eliminar_curso"),
]
