import os
import django
from datetime import datetime, timedelta
import random
import string

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studenthub.settings')
django.setup()

from student.models import Paciente, Especialidad, Medico, Cita, Receta

# Datos de ejemplo
NOMBRES = [
    "Juan", "María", "Carlos", "Ana", "Luis", "Patricia", "José", "Rosa", "Miguel", "Carmen",
    "Antonio", "Isabel", "Francisco", "Elena", "Manuel", "Dolores", "Pedro", "María José",
    "Diego", "Francisca", "Sergio", "Mercedes", "Andrés", "Beatriz", "Javier", "Pilar",
    "Alejandro", "Yolanda", "Roberto", "Silvia", "Fernando", "Asunción", "Ramón", "Consuelo",
    "Enrique", "Aurora", "Vicente", "Esperanza", "Ángel", "Soledad", "Eduardo", "Virtudes",
    "Julio", "Gloria", "Alberto", "Angélica", "Alfonso", "Fuensanta", "Arturo", "Sonsoles"
]

APELLIDOS = [
    "García", "Martínez", "Rodríguez", "Hernández", "López", "González", "Sánchez", "Pérez",
    "Díaz", "Ramírez", "Cruz", "Jiménez", "Moreno", "Gutiérrez", "Ortiz", "Vargas",
    "Castro", "Reyes", "Vega", "Medina", "Rojas", "Ruiz", "Espinoza", "Flores",
    "Navarro", "Ríos", "Soto", "Campos", "Acosta", "Gallardo", "Meza", "Figueroa",
    "Contreras", "Salazar", "Fuentes", "Carrasco", "Molina", "Miranda", "Muñoz", "Sandoval",
    "Pino", "Valencia", "Cisternas", "Bravo", "Arancibia", "Tapia", "Valenzuela", "Mansilla"
]

APELLIDO_PACIENTE = [
    "García López", "Martínez Sánchez", "Rodríguez Díaz", "Hernández Pérez", "López Ramírez",
    "González Cruz", "Sánchez Jiménez", "Pérez Moreno", "Díaz Gutiérrez", "Ramírez Ortiz"
]

def random_email():
    return f"user{random.randint(1000, 9999)}@email.com"

def random_phone():
    return f"09{random.randint(10000000, 99999999)}"

def random_date(days_back=365, days_forward=0):
    end = datetime.now() + timedelta(days=days_forward)
    start = end - timedelta(days=days_back)
    return start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))

def random_text(length=100):
    return ''.join(random.choices(string.ascii_letters + ' ', k=length))

def generar_especialidades(cantidad=50):
    """Generar especialidades médicas"""
    print("Generando Especialidades...")
    especialidades_nombres = [
        "Cardiología", "Dermatología", "Oftalmología", "Otorrinolaringología",
        "Pediatría", "Neurología", "Psiquiatría", "Endocrinología", "Gastroenterología",
        "Neumología", "Reumatología", "Urología", "Oncología", "Traumatología",
        "Cirugía General", "Anestesiología", "Radiología", "Patología", "Laboratorio Clínico",
        "Ginecología", "Obstetricia", "Medicina Interna", "Infectología", "Alergología",
        "Hematología", "Nefrología", "Neumología", "Ortopedia", "Oftalmología",
        "Estomatología", "Fisioterapia", "Nutrición", "Psicología", "Farmacología",
        "Toxicología", "Epidemiología", "Salud Pública", "Medicina Preventiva", "Cuidados Intensivos",
        "Angiología", "Flebología", "Proctología", "Coloproctología", "Andrología",
        "Sexología", "Tanatología", "Gerontología", "Podología", "Cosmetología"
    ]
    
    for i, nombre in enumerate(especialidades_nombres[:cantidad]):
        if not Especialidad.objects.filter(nombre=nombre).exists():
            Especialidad.objects.create(
                nombre=nombre,
                descripcion=f"Especialidad en {nombre}. Brindamos servicios de calidad en esta rama de la medicina."
            )
    print(f"✅ {min(cantidad, len(especialidades_nombres))} Especialidades creadas")


def generar_pacientes(cantidad=50):
    """Generar pacientes"""
    print("Generando Pacientes...")
    for i in range(cantidad):
        cedula = f"{random.randint(100000000, 999999999)}"
        if not Paciente.objects.filter(cedula=cedula).exists():
            usuario = f"paciente_{random.randint(1000, 9999)}"
            while Paciente.objects.filter(username=usuario).exists():
                usuario = f"paciente_{random.randint(1000, 9999)}"
            
            try:
                Paciente.objects.create_user(
                    username=usuario,
                    email=random_email(),
                    password='test123456',
                    first_name=random.choice(NOMBRES),
                    last_name=random.choice(APELLIDOS),
                    cedula=cedula,
                    telefono=random_phone(),
                    fecha_nacimiento=random_date(days_back=27375, days_forward=0).date(),
                    direccion=f"Calle {random.randint(1, 99)}, Apartamento {random.randint(1, 999)}"
                )
            except Exception as e:
                pass
    print(f"✅ {cantidad} Pacientes creados")


def generar_medicos(cantidad=50):
    """Generar médicos"""
    print("Generando Médicos...")
    especialidades = list(Especialidad.objects.all())
    if not especialidades:
        print("⚠️  No hay especialidades. Genera especialidades primero.")
        return
    
    creados = 0
    for i in range(cantidad):
        cedula = f"{random.randint(100000000, 999999999)}"
        if not Medico.objects.filter(cedula=cedula).exists():
            try:
                Medico.objects.create(
                    nombre=random.choice(NOMBRES),
                    apellido=random.choice(APELLIDOS),
                    cedula=cedula,
                    licencia=f"LIC{random.randint(100000, 999999)}",
                    telefono=random_phone(),
                    email=random_email(),
                    especialidad=random.choice(especialidades)
                )
                creados += 1
            except Exception as e:
                pass
    print(f"✅ {creados} Médicos creados")


def generar_citas(cantidad=50):
    """Generar citas médicas"""
    print("Generando Citas Médicas...")
    
    # Recargar los datos desde la BD
    pacientes = list(Paciente.objects.all())
    medicos = list(Medico.objects.all())
    
    print(f"   Pacientes encontrados: {len(pacientes)}")
    print(f"   Médicos encontrados: {len(medicos)}")
    
    if not pacientes or not medicos:
        print("⚠️  No hay pacientes o médicos. Genera esos datos primero.")
        return
    
    estados = ['pendiente', 'confirmada', 'realizada', 'cancelada']
    creadas = 0
    
    for i in range(cantidad):
        try:
            fecha = random_date(days_back=30, days_forward=30)
            Cita.objects.create(
                paciente=random.choice(pacientes),
                medico=random.choice(medicos),
                fecha=fecha,
                motivo="Consulta general",
                notas="Paciente refiere molestias generales",
                estado=random.choice(estados)
            )
            creadas += 1
        except Exception as e:
            print(f"   Error: {e}")
    print(f"✅ {creadas} Citas Médicas creadas")


def generar_recetas(cantidad=50):
    """Generar recetas médicas"""
    print("Generando Recetas Médicas...")
    
    # Recargar los datos desde la BD
    citas = list(Cita.objects.all())
    
    print(f"   Citas encontradas: {len(citas)}")
    
    if not citas:
        print("⚠️  No hay citas. Genera citas primero.")
        return
    
    medicamentos = [
        "Paracetamol", "Ibuprofeno", "Amoxicilina", "Azitromicina", "Omeprazol",
        "Metformina", "Enalapril", "Atorvastatina", "Losartán", "Furosemida",
        "Espironolactona", "Digoxina", "Warfarina", "Clopidogrel", "Aspirin",
        "Fluoxetina", "Sertralina", "Escitalopram", "Alprazolam", "Clonazepam",
        "Lorazepam", "Diazepam", "Midazolam", "Zolpidem", "Melatonina",
        "Cetirizina", "Loratadina", "Fexofenadina", "Montelukast", "Salbutamol",
        "Formoterol", "Tiotropio", "Prednisona", "Dexametasona", "Hidrocortisona",
        "Levotiroxina", "Liothyronine", "Insulina", "Glibenclamida", "Repaglinida",
        "Acarbosa", "Sitagliptina", "Vildagliptina", "Pioglitazona", "Gemfibrozilo",
        "Ezetimiba", "Niacina", "Clopidogrel", "Enoxaparina", "Heparina"
    ]
    
    frecuencias = ['Cada 4 horas', 'Cada 6 horas', 'Cada 8 horas', 'Cada 12 horas', 
                   'Una vez al día', 'Dos veces al día', 'Tres veces al día']
    
    creadas = 0
    for i in range(cantidad):
        try:
            Receta.objects.create(
                cita=random.choice(citas),
                medicamento=random.choice(medicamentos),
                dosis=f"{random.choice([250, 500, 1000, 2000])} mg",
                frecuencia=random.choice(frecuencias),
                duracion=f"{random.randint(5, 30)} días",
                indicaciones="Tomar según indicaciones. Consultar si hay efectos secundarios."
            )
            creadas += 1
        except Exception as e:
            pass
    print(f"✅ {creadas} Recetas Médicas creadas")


if __name__ == '__main__':
    print("=" * 60)
    print("GENERADOR DE DATOS - PacienteHub")
    print("=" * 60)
    
    # Generar en orden de dependencias
    generar_especialidades(50)
    generar_pacientes(50)
    generar_medicos(50)
    
    # Recargar los objetos de la base de datos
    from django.db import connection
    connection.close()
    
    generar_citas(50)
    generar_recetas(50)
    
    print("=" * 60)
    print("✅ ¡Todos los datos han sido generados correctamente!")
    print("=" * 60)
