import logging

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Paciente, Especialidad, Medico, Cita, Receta
from .forms import PacienteForm, LoginForm, RegistroForm, EspecialidadForm, MedicoForm, CitaForm, RecetaForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout

logger = logging.getLogger(__name__)
# Create your views here.

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('student:inicio')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('student:login')

def register_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            try:
                nombre = user.first_name or user.username
                cuerpo = (
                    f"Hola {nombre},\n\n"
                    "Tu cuenta en PacienteHub se creó correctamente. "
                    "Ahora puedes iniciar sesión y administrar tus datos médicos.\n\n"
                    "Gracias por registrarte."
                )
                send_mail(
                    subject='Bienvenido a PacienteHub',
                    message=cuerpo,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
            except Exception as exc:  # pragma: no cover - se loguea para depuración
                logger.warning('No se pudo enviar correo de bienvenida: %s', exc)
                messages.warning(
                    request,
                    'La cuenta fue creada pero no se pudo enviar el correo de confirmación.',
                )
            else:
                messages.success(request, 'Cuenta creada con éxito. Revisa tu correo de confirmación.')
            login(request, user)
            return redirect('student:inicio')
    else:
        form = RegistroForm()
    
    return render(request, 'registro.html', {'form': form})

@login_required(login_url='student:login')
def inicio(request):
    pacientes = Paciente.objects.all()
    return render(request, 'inicio.html', {'pacientes': pacientes})

@login_required(login_url='student:login')
def listar_pacientes(request):
    pacientes = Paciente.objects.all()
    
    return render(request, 'paciente/listar.html', {'pacientes': pacientes})

@login_required(login_url='student:login')
def crear_paciente(request):
    form = PacienteForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Paciente creado correctamente')
        return redirect('student:listar_pacientes')
    
    return render(request, 'paciente/crear.html', {'form': form})

@login_required(login_url='student:login')
def editar_paciente(request, slug):
    paciente = get_object_or_404(Paciente, slug=slug)
    form = PacienteForm(request.POST or None, instance=paciente)
    if form.is_valid():
        form.save()
        messages.success(request, 'Paciente actualizado correctamente')
        return redirect('student:listar_pacientes')
    
    return render(request, 'paciente/editar.html', {'form': form, 'paciente': paciente})

@login_required(login_url='student:login')
def eliminar_paciente(request, slug):
    paciente = get_object_or_404(Paciente, slug=slug)
    if request.method == 'POST':
        paciente.delete()
        messages.success(request, 'Paciente eliminado correctamente')
        return redirect('student:listar_pacientes')
    
    return render(request, 'paciente/eliminar.html', {'paciente': paciente})


# ===== CRUD ESPECIALIDAD =====
@login_required(login_url='student:login')
def listar_especialidades(request):
    especialidades = Especialidad.objects.all()
    return render(request, 'especialidad/listar.html', {'especialidades': especialidades})

@login_required(login_url='student:login')
def crear_especialidad(request):
    form = EspecialidadForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Especialidad creada correctamente')
        return redirect('student:listar_especialidades')
    return render(request, 'especialidad/crear.html', {'form': form})

@login_required(login_url='student:login')
def editar_especialidad(request, slug):
    especialidad = get_object_or_404(Especialidad, slug=slug)
    form = EspecialidadForm(request.POST or None, instance=especialidad)
    if form.is_valid():
        form.save()
        messages.success(request, 'Especialidad actualizada correctamente')
        return redirect('student:listar_especialidades')
    return render(request, 'especialidad/editar.html', {'form': form, 'especialidad': especialidad})

@login_required(login_url='student:login')
def eliminar_especialidad(request, slug):
    especialidad = get_object_or_404(Especialidad, slug=slug)
    if request.method == 'POST':
        especialidad.delete()
        messages.success(request, 'Especialidad eliminada correctamente')
        return redirect('student:listar_especialidades')
    return render(request, 'especialidad/eliminar.html', {'especialidad': especialidad})


# ===== CRUD MEDICO =====
@login_required(login_url='student:login')
def listar_medicos(request):
    medicos = Medico.objects.all()
    return render(request, 'medico/listar.html', {'medicos': medicos})

@login_required(login_url='student:login')
def crear_medico(request):
    form = MedicoForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Médico creado correctamente')
        return redirect('student:listar_medicos')
    return render(request, 'medico/crear.html', {'form': form})

@login_required(login_url='student:login')
def editar_medico(request, slug):
    medico = get_object_or_404(Medico, slug=slug)
    form = MedicoForm(request.POST or None, instance=medico)
    if form.is_valid():
        form.save()
        messages.success(request, 'Médico actualizado correctamente')
        return redirect('student:listar_medicos')
    return render(request, 'medico/editar.html', {'form': form, 'medico': medico})

@login_required(login_url='student:login')
def eliminar_medico(request, slug):
    medico = get_object_or_404(Medico, slug=slug)
    if request.method == 'POST':
        medico.delete()
        messages.success(request, 'Médico eliminado correctamente')
        return redirect('student:listar_medicos')
    return render(request, 'medico/eliminar.html', {'medico': medico})


# ===== CRUD CITA =====
@login_required(login_url='student:login')
def listar_citas(request):
    citas = Cita.objects.all()
    return render(request, 'cita/listar.html', {'citas': citas})

@login_required(login_url='student:login')
def crear_cita(request):
    form = CitaForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Cita creada correctamente')
        return redirect('student:listar_citas')
    return render(request, 'cita/crear.html', {'form': form})

@login_required(login_url='student:login')
def editar_cita(request, slug):
    cita = get_object_or_404(Cita, slug=slug)
    form = CitaForm(request.POST or None, instance=cita)
    if form.is_valid():
        form.save()
        messages.success(request, 'Cita actualizada correctamente')
        return redirect('student:listar_citas')
    return render(request, 'cita/editar.html', {'form': form, 'cita': cita})

@login_required(login_url='student:login')
def eliminar_cita(request, slug):
    cita = get_object_or_404(Cita, slug=slug)
    if request.method == 'POST':
        cita.delete()
        messages.success(request, 'Cita eliminada correctamente')
        return redirect('student:listar_citas')
    return render(request, 'cita/eliminar.html', {'cita': cita})


# ===== CRUD RECETA =====
@login_required(login_url='student:login')
def listar_recetas(request):
    recetas = Receta.objects.all()
    return render(request, 'receta/listar.html', {'recetas': recetas})

@login_required(login_url='student:login')
def crear_receta(request):
    form = RecetaForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Receta creada correctamente')
        return redirect('student:listar_recetas')
    return render(request, 'receta/crear.html', {'form': form})

@login_required(login_url='student:login')
def editar_receta(request, slug):
    receta = get_object_or_404(Receta, slug=slug)
    form = RecetaForm(request.POST or None, instance=receta)
    if form.is_valid():
        form.save()
        messages.success(request, 'Receta actualizada correctamente')
        return redirect('student:listar_recetas')
    return render(request, 'receta/editar.html', {'form': form, 'receta': receta})

@login_required(login_url='student:login')
def eliminar_receta(request, slug):
    receta = get_object_or_404(Receta, slug=slug)
    if request.method == 'POST':
        receta.delete()
        messages.success(request, 'Receta eliminada correctamente')
        return redirect('student:listar_recetas')
    return render(request, 'receta/eliminar.html', {'receta': receta})
    
    
    
        
    
