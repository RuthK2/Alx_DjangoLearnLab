import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from django.contrib import admin
from django.contrib.auth.models import User
from relationship_app.models import CustomUser

print("Registered models in admin:")
for model, admin_class in admin.site._registry.items():
    print(f"- {model.__name__}: {admin_class.__class__.__name__}")

print(f"\nDefault User model registered: {User in admin.site._registry}")
print(f"CustomUser model registered: {CustomUser in admin.site._registry}")