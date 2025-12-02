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
    
    def test_registration_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'csrfmiddlewaretoken')
    
    def test_registration_post(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'newpass123',
            'password2': 'newpass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_login_required_profile(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)
    
    def test_login_required_edit_profile(self):
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code, 302)
    
    def test_profile_access_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
    
    def test_logout_functionality(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
    
    def test_password_hashing(self):
        user = User.objects.get(username='testuser')
        self.assertNotEqual(user.password, 'testpass123')
        self.assertTrue(user.password.startswith('pbkdf2_'))