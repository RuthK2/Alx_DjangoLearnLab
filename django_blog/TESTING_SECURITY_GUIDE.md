# Django Blog Authentication Testing & Security Guide

## Testing Functionalities

### 1. Registration Testing
```bash
# Start development server
python manage.py runserver

# Test registration at: http://127.0.0.1:8000/register/
```
**Test Cases:**
- Valid registration with username, email, password
- Duplicate username handling
- Password confirmation mismatch
- Email validation
- Auto-login after successful registration

### 2. Login Testing
```bash
# Test login at: http://127.0.0.1:8000/login/
```
**Test Cases:**
- Valid credentials login
- Invalid credentials handling
- Redirect to profile after login
- Login required for protected views

### 3. Logout Testing
```bash
# Test logout at: http://127.0.0.1:8000/logout/
```
**Test Cases:**
- Successful logout and redirect
- Session termination
- Access to protected views after logout

### 4. Profile Management Testing
```bash
# Test profile at: http://127.0.0.1:8000/profile/
# Test edit at: http://127.0.0.1:8000/profile/edit/
```
**Test Cases:**
- View profile information
- Edit profile fields
- Form validation
- Unauthorized access prevention

## Security Verification

### 1. CSRF Protection Check
**Verify CSRF tokens in templates:**
```html
<!-- All forms should include: -->
{% csrf_token %}
```

**Check in browser:**
- Inspect form elements for `csrfmiddlewaretoken` hidden input
- Verify 403 error when CSRF token is missing

### 2. Password Security Verification
**Django automatically handles:**
- Password hashing using PBKDF2
- Salt generation
- Secure password storage

**Verify in Django shell:**
```python
python manage.py shell
from django.contrib.auth.models import User
user = User.objects.get(username='testuser')
print(user.password)  # Should show hashed password
```

### 3. Authentication Security Tests
**Manual Security Tests:**
- Try accessing `/profile/` without login → Should redirect to login
- Try accessing `/profile/edit/` without login → Should redirect to login
- Verify logout terminates session
- Check password requirements are enforced

## Automated Testing

### Create Test File
```python
# blog/test_auth.py
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

class AuthTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'newpass123',
            'password2': 'newpass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_login_required(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)
    
    def test_csrf_protection(self):
        response = self.client.post(reverse('register'), {})
        self.assertContains(response, 'csrfmiddlewaretoken')
```

### Run Tests
```bash
python manage.py test blog.test_auth
```

## Security Checklist

### ✅ CSRF Protection
- [x] All forms include `{% csrf_token %}`
- [x] CSRF middleware enabled in settings
- [x] Forms reject requests without valid CSRF tokens

### ✅ Password Security
- [x] Django's built-in password hashing (PBKDF2)
- [x] Passwords never stored in plain text
- [x] Secure password validation

### ✅ Authentication Security
- [x] `@login_required` decorators on protected views
- [x] Proper session management
- [x] Secure logout functionality

### ✅ Form Validation
- [x] Server-side validation for all inputs
- [x] Email format validation
- [x] Password confirmation matching

## Common Security Issues to Avoid

### ❌ Don't Do:
- Store passwords in plain text
- Skip CSRF tokens in forms
- Allow access to protected views without authentication
- Trust client-side validation only

### ✅ Do:
- Use Django's built-in authentication
- Include CSRF tokens in all forms
- Validate all inputs server-side
- Use `@login_required` for protected views

## Production Security Settings

### Additional Settings for Production:
```python
# settings.py
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

## Testing Commands Summary
```bash
# Run development server
python manage.py runserver

# Run automated tests
python manage.py test

# Check for security issues
python manage.py check --deploy

# Create superuser for admin testing
python manage.py createsuperuser
```