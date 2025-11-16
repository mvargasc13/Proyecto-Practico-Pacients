from django.contrib import admin
from .models import Paciente, Especialidad, Medico, Cita, Receta

class PacienteAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name", "cedula", "email", "telefono", "fecha_nacimiento", "direccion")
    search_fields = ("username", "first_name", "last_name", "cedula", "email")

admin.site.register(Paciente, PacienteAdmin)


class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ("nombre", "descripcion")
    search_fields = ("nombre",)

admin.site.register(Especialidad, EspecialidadAdmin)


class MedicoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "apellido", "cedula", "especialidad", "email", "telefono", "licencia")
    search_fields = ("nombre", "apellido", "cedula", "licencia", "email")
    list_filter = ("especialidad",)

admin.site.register(Medico, MedicoAdmin)


class CitaAdmin(admin.ModelAdmin):
    list_display = ("paciente", "medico", "fecha", "estado", "motivo")
    search_fields = ("paciente__first_name", "medico__nombre", "motivo")
    list_filter = ("estado", "fecha")

admin.site.register(Cita, CitaAdmin)


class RecetaAdmin(admin.ModelAdmin):
    list_display = ("medicamento", "cita", "dosis", "frecuencia", "duracion")
    search_fields = ("medicamento", "cita__id")

admin.site.register(Receta, RecetaAdmin)
