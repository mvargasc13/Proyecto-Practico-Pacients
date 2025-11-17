from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser


class Paciente(AbstractUser):
    cedula = models.CharField(max_length=10, unique=True)
    telefono = models.CharField(max_length=10)
    fecha_nacimiento = models.DateField()
    direccion = models.TextField()

    #campos obligatorios
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.cedula}"

    # Alias para mantener compatibilidad con templates y formularios existentes
    @property
    def nombres(self):
        return self.first_name

    @property
    def apellidos(self):
        return self.last_name

    @property
    def correo(self):
        return self.email


class Especialidad(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Especialidades"


class Medico(models.Model):
    cedula = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=10)
    licencia = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.nombre}-{self.cedula}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.especialidad.nombre}"


class Cita(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('realizada', 'Realizada'),
        ('cancelada', 'Cancelada'),
    ]

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    motivo = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    notas = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils import timezone
            timestamp = timezone.now().timestamp()
            self.slug = slugify(f"cita-{self.paciente.id}-{self.medico.id}-{timestamp}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Cita: {self.paciente.first_name} con Dr. {self.medico.nombre} - {self.fecha}"

    class Meta:
        ordering = ['-fecha']


class Receta(models.Model):
    cita = models.ForeignKey(Cita, on_delete=models.CASCADE)
    medicamento = models.CharField(max_length=150)
    dosis = models.CharField(max_length=100)
    frecuencia = models.CharField(max_length=100)
    duracion = models.CharField(max_length=100)
    indicaciones = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils import timezone
            timestamp = timezone.now().timestamp()
            self.slug = slugify(f"receta-{self.cita.id}-{timestamp}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Receta: {self.medicamento} - Cita {self.cita.id}"

