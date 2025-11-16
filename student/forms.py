from django import forms
from .models import Paciente, Especialidad, Medico, Cita, Receta
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import EmailValidator
from django.contrib.auth.forms import AuthenticationForm
from django.forms import DateInput, DateTimeInput

Usuario = get_user_model()

class LoginForm(AuthenticationForm):
    
    pass


class RegistroForm(UserCreationForm):

    class Meta:
        model = Usuario
        fields = [
            'username', 'cedula', 'first_name', 'last_name', 'email',
            'telefono', 'fecha_nacimiento', 'direccion', 'password1', 'password2'
        ]
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'})
        }

    def clean_cedula(self):
        cedula = self.cleaned_data.get("cedula", "").strip()

        if not cedula.isdigit():
            raise forms.ValidationError("La cédula solo debe contener números")

        if len(cedula) != 10:
            raise forms.ValidationError("La cédula debe tener exactamente 10 dígitos")

        provincia = int(cedula[:2])
        if provincia < 1 or provincia > 24:
            raise forms.ValidationError("La cédula debe comenzar con un código de provincia válido (01-24)")

        if Usuario.objects.filter(cedula=cedula).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Ya existe un usuario con esta cédula")

        return cedula

    def clean_first_name(self):
        nombres = self.cleaned_data.get("first_name", "").strip()

        if len(nombres) == 0:
            raise forms.ValidationError("El campo está vacío")

        if not all(char.isalpha() or char.isspace() for char in nombres):
            raise forms.ValidationError("El nombre solo debe contener letras y espacios")

        return nombres

    def clean_last_name(self):
        apellidos = self.cleaned_data.get("last_name", "").strip()

        if len(apellidos) == 0:
            raise forms.ValidationError("El campo está vacío")

        if not all(char.isalpha() or char.isspace() for char in apellidos):
            raise forms.ValidationError("Los apellidos solo deben contener letras y espacios")

        return apellidos

    def clean_email(self):
        email = self.cleaned_data.get("email", "").strip().lower()

        if not email:
            raise forms.ValidationError("Este campo es obligatorio")

        validator = EmailValidator(message="Ingrese un correo electrónico válido")
        try:
            validator(email)
        except forms.ValidationError:
            raise forms.ValidationError("El formato del correo no es válido")

        if Usuario.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Ya existe un usuario con este correo")

        return email

    def clean_telefono(self):
        telefono = self.cleaned_data.get("telefono", "").strip()

        if not telefono:
            raise forms.ValidationError("El campo está vacío")

        if not telefono.isdigit():
            raise forms.ValidationError("El teléfono solo debe contener números")

        if not telefono.startswith("09"):
            raise forms.ValidationError("El teléfono debe comenzar con 09")

        if len(telefono) != 10:
            raise forms.ValidationError("El teléfono debe tener exactamente 10 números")

        return telefono

    def clean_fecha_nacimiento(self):
        fecha = self.cleaned_data.get("fecha_nacimiento")

        if not fecha:
            raise forms.ValidationError("El campo está vacío")

        return fecha

    def clean_direccion(self):
        direccion = self.cleaned_data.get("direccion", "").strip()

        if not direccion:
            raise forms.ValidationError("El campo está vacío")

        return direccion
    
class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['cedula', 'first_name', 'last_name', 'email', 'telefono', 'fecha_nacimiento', 'direccion']
        widgets = {'fecha_nacimiento': DateInput(attrs={'type': 'date'})}

    def clean_cedula(self):
        cedula = self.cleaned_data.get("cedula", "").strip()

        if not cedula.isdigit():
            raise forms.ValidationError("La cédula solo debe contener números")

        if len(cedula) != 10:
            raise forms.ValidationError("La cédula debe tener exactamente 10 dígitos")

        provincia = int(cedula[:2])
        if provincia < 1 or provincia > 24:
            raise forms.ValidationError("La cédula debe comenzar con un código de provincia válido (01-24)")

        if Paciente.objects.filter(cedula=cedula).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Ya existe un paciente con esta cédula")

        return cedula

    def clean_first_name(self):
        nombres = self.cleaned_data.get("first_name", "").strip()

        if len(nombres) == 0:
            raise forms.ValidationError("El campo está vacío")

        if not all(char.isalpha() or char.isspace() for char in nombres):
            raise forms.ValidationError("El nombre solo debe contener letras y espacios")

        return nombres

    def clean_last_name(self):
        apellidos = self.cleaned_data.get("last_name", "").strip()

        if len(apellidos) == 0:
            raise forms.ValidationError("El campo está vacío")

        if not all(char.isalpha() or char.isspace() for char in apellidos):
            raise forms.ValidationError("Los apellidos solo deben contener letras y espacios")

        return apellidos

    def clean_email(self):
        correo = self.cleaned_data.get("email", "").strip().lower()

        if not correo:
            raise forms.ValidationError("Este campo es obligatorio")

        validator = EmailValidator(message="Ingrese un correo electrónico válido")
        try:
            validator(correo)
        except forms.ValidationError:
            raise forms.ValidationError("El formato del correo no es válido")

        if Paciente.objects.filter(email=correo).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Ya existe un paciente registrado con este correo")

        return correo

    def clean_telefono(self):
        telefono = self.cleaned_data.get("telefono")

        if not telefono:
            raise forms.ValidationError("El campo está vacío")

        telefono = telefono.strip()

        if not telefono.isdigit():
            raise forms.ValidationError("El teléfono solo debe contener números")

        if not telefono.startswith("09"):
            raise forms.ValidationError("El teléfono debe comenzar con 09")

        if len(telefono) != 10:
            raise forms.ValidationError("El teléfono debe tener exactamente 10 números")

        return telefono

    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data.get("fecha_nacimiento")

        if not fecha_nacimiento:
            raise forms.ValidationError("El campo está vacío")

        return fecha_nacimiento

    def clean_direccion(self):
        direccion = self.cleaned_data.get("direccion")

        if not direccion:
            raise forms.ValidationError("El campo está vacío")

        return direccion


class EspecialidadForm(forms.ModelForm):
    class Meta:
        model = Especialidad
        fields = ['nombre', 'descripcion']

    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre", "").strip()

        if not nombre:
            raise forms.ValidationError("El nombre es obligatorio")

        if not all(char.isalpha() or char.isspace() for char in nombre):
            raise forms.ValidationError("El nombre solo debe contener letras")

        return nombre


class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['cedula', 'nombre', 'apellido', 'especialidad', 'email', 'telefono', 'licencia']

    def clean_cedula(self):
        cedula = self.cleaned_data.get("cedula", "").strip()

        if not cedula.isdigit():
            raise forms.ValidationError("La cédula solo debe contener números")

        if len(cedula) != 10:
            raise forms.ValidationError("La cédula debe tener exactamente 10 dígitos")

        provincia = int(cedula[:2])
        if provincia < 1 or provincia > 24:
            raise forms.ValidationError("La cédula debe comenzar con un código de provincia válido (01-24)")

        if Medico.objects.filter(cedula=cedula).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Ya existe un médico con esta cédula")

        return cedula

    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre", "").strip()

        if not nombre:
            raise forms.ValidationError("El nombre es obligatorio")

        if not all(char.isalpha() or char.isspace() for char in nombre):
            raise forms.ValidationError("El nombre solo debe contener letras")

        return nombre

    def clean_apellido(self):
        apellido = self.cleaned_data.get("apellido", "").strip()

        if not apellido:
            raise forms.ValidationError("El apellido es obligatorio")

        if not all(char.isalpha() or char.isspace() for char in apellido):
            raise forms.ValidationError("El apellido solo debe contener letras")

        return apellido

    def clean_email(self):
        email = self.cleaned_data.get("email", "").strip().lower()

        if not email:
            raise forms.ValidationError("El email es obligatorio")

        validator = EmailValidator(message="Ingrese un correo válido")
        try:
            validator(email)
        except forms.ValidationError:
            raise forms.ValidationError("El formato del correo no es válido")

        if Medico.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Ya existe un médico con este email")

        return email

    def clean_telefono(self):
        telefono = self.cleaned_data.get("telefono", "").strip()

        if not telefono:
            raise forms.ValidationError("El teléfono es obligatorio")

        if not telefono.isdigit():
            raise forms.ValidationError("El teléfono solo debe contener números")

        if not telefono.startswith("09"):
            raise forms.ValidationError("El teléfono debe comenzar con 09")

        if len(telefono) != 10:
            raise forms.ValidationError("El teléfono debe tener exactamente 10 números")

        return telefono

    def clean_licencia(self):
        licencia = self.cleaned_data.get("licencia", "").strip()

        if not licencia:
            raise forms.ValidationError("La licencia es obligatoria")

        if Medico.objects.filter(licencia=licencia).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Ya existe un médico con esta licencia")

        return licencia


class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['paciente', 'medico', 'fecha', 'motivo', 'estado', 'notas']
        widgets = {'fecha': DateTimeInput(attrs={'type': 'datetime-local'})}

    def clean_motivo(self):
        motivo = self.cleaned_data.get("motivo", "").strip()

        if not motivo:
            raise forms.ValidationError("El motivo es obligatorio")

        return motivo


class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = ['cita', 'medicamento', 'dosis', 'frecuencia', 'duracion', 'indicaciones']

    def clean_medicamento(self):
        medicamento = self.cleaned_data.get("medicamento", "").strip()

        if not medicamento:
            raise forms.ValidationError("El medicamento es obligatorio")

        return medicamento

    def clean_dosis(self):
        dosis = self.cleaned_data.get("dosis", "").strip()

        if not dosis:
            raise forms.ValidationError("La dosis es obligatoria")

        return dosis

    def clean_frecuencia(self):
        frecuencia = self.cleaned_data.get("frecuencia", "").strip()

        if not frecuencia:
            raise forms.ValidationError("La frecuencia es obligatoria")

        return frecuencia

    def clean_duracion(self):
        duracion = self.cleaned_data.get("duracion", "").strip()

        if not duracion:
            raise forms.ValidationError("La duración es obligatoria")

        return duracion
