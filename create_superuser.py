import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import User

if not User.objects.filter(email='admin@achievers.lk').exists():
    User.objects.create_superuser(
        email='admin@achievers.lk',
        password='admin123',
        first_name='Admin',
        last_name='User',
        role='super_admin'
    )
    print("Superuser created successfully!")
    print("Email: admin@achievers.lk")
    print("Password: admin123")
else:
    print("Superuser already exists!")
