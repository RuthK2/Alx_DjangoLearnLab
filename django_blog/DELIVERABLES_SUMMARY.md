# Django Blog Authentication System - Deliverables

## Code Files

### 1. Authentication Views (`blog/views.py`)
```python
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, EditProfileForm

def home(request):
    return render(request,'base.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
             password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'registration/profile.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'registration/edit_profile.html', {'form': form})
```

### 2. Authentication Forms (`blog/forms.py`)
```python
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
```

### 3. URL Configuration (`blog/urls.py`)
```python
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import home, register, profile, logout_view, edit_profile

urlpatterns = [
    path('', home, name='home'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
]
```

### 4. Settings Configuration (`django_blog/settings.py`)
```python
# Login redirect settings
LOGIN_REDIRECT_URL = '/profile/'
LOGOUT_REDIRECT_URL = '/'

# Template configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/ 'blog'/ 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Static files configuration
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'blog'/ 'static']
```

## Template Files

### 1. Base Template (`blog/templates/base.html`)
```html
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Django Blog{% endblock %}</title>
    <link rel="stylesheet" href="{% static 'blog/styles.css' %}">
</head>
<body>
    <h1>Welcome to the Django Blog</h1>
    <header>
        <nav>
            <ul>
                <li><a href="{% url 'home' %}">Home</a></li>
                {% if user.is_authenticated %}
                    <li><a href="{% url 'profile' %}">Profile</a></li>
                    <li><a href="{% url 'logout' %}">Logout</a></li>
                {% else %}
                    <li><a href="{% url 'login' %}">Login</a></li>
                    <li><a href="{% url 'register' %}">Register</a></li>
                {% endif %}
            </ul>
        </nav>
    </header>

    <div class="content">
        {% block content %}
        <!-- Page-specific content goes here -->
        {% endblock %}
    </div>

    <footer>
        <p>&copy; 2024 Django Blog</p>
    </footer>

    <script src="{% static 'blog/scripts.js' %}"></script>
</body>
</html>
```

### 2. Login Template (`blog/templates/registration/login.html`)
```html
{% extends "base.html" %}
{% load static %}

{% block content %}
<link rel="stylesheet" href="{% static 'blog/login.css' %}">
<div class="auth-container">
    <h2>Login</h2>
    
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Login</button>
    </form>
    
    <p>Don't have an account? <a href="{% url 'register' %}">Register</a></p>
</div>
{% endblock %}
```

### 3. Register Template (`blog/templates/registration/register.html`)
```html
{% extends "base.html" %}
{% load static %}

{% block content %}
<link rel="stylesheet" href="{% static 'blog/register.css' %}">
<div class="auth-container">
    <h2>Create Account</h2>
    
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Register</button>
    </form>
    
    <p>Already registered? <a href="{% url 'login' %}">Login</a></p>
</div>
{% endblock %}
```

### 4. Profile Template (`blog/templates/registration/profile.html`)
```html
{% extends "base.html" %}

{% block title %}Your Profile | Django Blog{% endblock %}

{% block content %}
<div class="auth-container">
    <h2>Your Profile</h2>

    <p><strong>Username:</strong> {{ user.username }}</p>
    <p><strong>Email:</strong> {{ user.email }}</p>
    <p><strong>Member Since:</strong> {{ user.date_joined|date:"F j, Y" }}</p>

    <a class="btn" href="{% url 'edit_profile' %}">Edit Profile</a>
    <a class="btn" href="{% url 'logout' %}">Logout</a>
</div>
{% endblock %}
```

### 5. Edit Profile Template (`blog/templates/registration/edit_profile.html`)
```html
{% extends 'base.html' %}

{% block content %}
<div class="auth-container">
    <h2>Edit Profile</h2>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Update Profile</button>
    </form>
    <a href="{% url 'profile' %}">Back to Profile</a>
</div>
{% endblock %}
```

### 6. Logout Template (`blog/templates/registration/logout.html`)
```html
{% extends "base.html" %}

{% block content %}
<div class="auth-container">
    <h2>Logged Out</h2>
    <p>You have been successfully logged out.</p>
    <a href="{% url 'login' %}">Login Again</a>
    <a href="{% url 'home' %}">Home</a>
</div>
{% endblock %}
```

## Static Files

### 1. Main Styles (`blog/Static/blog/styles.css`)
- General authentication form styling
- Layout and responsive design
- Button and input field styles

### 2. Login Styles (`blog/Static/blog/login.css`)
- Login form specific styling
- Form validation styles

### 3. Register Styles (`blog/Static/blog/register.css`)
- Registration form specific styling
- Error message styling

## Documentation

### 1. Complete System Documentation
- **File**: `AUTHENTICATION_DOCUMENTATION.md`
- **Contents**: Detailed system architecture, user workflows, security features

### 2. Testing & Security Guide
- **File**: `TESTING_SECURITY_GUIDE.md`
- **Contents**: Testing procedures, security verification, automated tests

### 3. Setup Instructions
- **File**: `DELIVERABLES_SUMMARY.md` (this file)
- **Contents**: Complete code listings, setup steps, usage guide

## Setup Instructions

### 1. Install Dependencies
```bash
pip install django
```

### 2. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 4. Run Development Server
```bash
python manage.py runserver
```

### 5. Access Authentication URLs
- Home: http://127.0.0.1:8000/
- Login: http://127.0.0.1:8000/login/
- Register: http://127.0.0.1:8000/register/
- Profile: http://127.0.0.1:8000/profile/
- Edit Profile: http://127.0.0.1:8000/profile/edit/

## Testing

### Run Automated Tests
```bash
python manage.py test blog.test_auth
python manage.py test blog.test_edit_profile
```

### Security Verification
- CSRF tokens in all forms
- Password hashing with PBKDF2
- Login required decorators
- Proper session management

## Features Implemented

✅ User Registration with email field
✅ User Login/Logout functionality
✅ Profile viewing and editing
✅ CSRF protection on all forms
✅ Secure password handling
✅ Responsive CSS styling
✅ Comprehensive testing suite
✅ Complete documentation
✅ Security best practices