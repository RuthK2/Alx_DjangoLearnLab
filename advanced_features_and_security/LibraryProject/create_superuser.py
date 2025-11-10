import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from bookshelf.models import CustomUser

# Create superuser
if not CustomUser.objects.filter(email='admin@example.com').exists():
    CustomUser.objects.create_superuser(
        email='admin@example.com',
        username='admin',
        password='admin123'
    )
    print("Superuser created: admin@example.com / admin123")
else:
    print("Superuser already exists")