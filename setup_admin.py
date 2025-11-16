import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studenthub.settings')
django.setup()

from student.models import Paciente

try:
    admin = Paciente.objects.get(username='admin')
    admin.is_staff = True
    admin.is_superuser = True
    admin.save()
    print(f"✅ Usuario 'admin' actualizado:")
    print(f"   - is_staff: {admin.is_staff}")
    print(f"   - is_superuser: {admin.is_superuser}")
except Paciente.DoesNotExist:
    print("❌ El usuario 'admin' no existe. Creando uno nuevo...")
    admin = Paciente.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123'
    )
    print(f"✅ Usuario 'admin' creado correctamente:")
    print(f"   - Nombre de usuario: admin")
    print(f"   - Contraseña: admin123")
    print(f"   - is_staff: {admin.is_staff}")
    print(f"   - is_superuser: {admin.is_superuser}")
