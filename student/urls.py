from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = 'student'

urlpatterns = [
    # ruta raíz: redirige a la vista de login
    path("", RedirectView.as_view(pattern_name='student:login', permanent=False), name='root'),
    # inicio disponible en /inicio/
    path("inicio/", views.inicio, name="inicio"),
    
    # PACIENTE
    path("paciente/crear/", views.crear_paciente, name="crear_paciente"),
    path("paciente/listar/", views.listar_pacientes, name="listar_pacientes"),
    path("paciente/editar/<slug:slug>/", views.editar_paciente, name="editar_paciente"),
    path("paciente/eliminar/<slug:slug>/", views.eliminar_paciente, name="eliminar_paciente"),
    
    # ESPECIALIDAD
    path("especialidad/crear/", views.crear_especialidad, name="crear_especialidad"),
    path("especialidad/listar/", views.listar_especialidades, name="listar_especialidades"),
    path("especialidad/editar/<slug:slug>/", views.editar_especialidad, name="editar_especialidad"),
    path("especialidad/eliminar/<slug:slug>/", views.eliminar_especialidad, name="eliminar_especialidad"),
    
    # MEDICO
    path("medico/crear/", views.crear_medico, name="crear_medico"),
    path("medico/listar/", views.listar_medicos, name="listar_medicos"),
    path("medico/editar/<slug:slug>/", views.editar_medico, name="editar_medico"),
    path("medico/eliminar/<slug:slug>/", views.eliminar_medico, name="eliminar_medico"),
    
    # CITA
    path("cita/crear/", views.crear_cita, name="crear_cita"),
    path("cita/listar/", views.listar_citas, name="listar_citas"),
    path("cita/editar/<slug:slug>/", views.editar_cita, name="editar_cita"),
    path("cita/eliminar/<slug:slug>/", views.eliminar_cita, name="eliminar_cita"),
    
    # RECETA
    path("receta/crear/", views.crear_receta, name="crear_receta"),
    path("receta/listar/", views.listar_recetas, name="listar_recetas"),
    path("receta/editar/<slug:slug>/", views.editar_receta, name="editar_receta"),
    path("receta/eliminar/<slug:slug>/", views.eliminar_receta, name="eliminar_receta"),
    
    # AUTH
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
]
