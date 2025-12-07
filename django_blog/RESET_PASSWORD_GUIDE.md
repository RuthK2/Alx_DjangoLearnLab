# Password Reset Guide

## Option 1: Reset Password via Django Shell (Quickest)

```bash
cd c:\Users\Belle\Alx_DjangoLearnLab\django_blog
python manage.py shell
```

Then run:
```python
from django.contrib.auth.models import User
user = User.objects.get(username='YOUR_USERNAME')
user.set_password('new_password123')
user.save()
exit()
```

## Option 2: Change Password via Command Line

```bash
python manage.py changepassword YOUR_USERNAME
```

Enter new password when prompted.

## Option 3: Create New Superuser

```bash
python manage.py createsuperuser
```

Follow prompts to create a new account.
