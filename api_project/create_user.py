import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_project.settings')
django.setup()

from django.contrib.auth.models import User

# Create superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'password123')
    print("Superuser created: admin/password123")
else:
    print("Superuser already exists")

# Create regular user for testing
if not User.objects.filter(username='testuser').exists():
    User.objects.create_user('testuser', 'test@example.com', 'testpass123')
    print("Test user created: testuser/testpass123")
else:
    print("Test user already exists")