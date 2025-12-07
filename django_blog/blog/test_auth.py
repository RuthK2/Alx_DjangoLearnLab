from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
import os

class AuthTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_password = os.environ.get('TEST_PASSWORD', 'testpass123')
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password=self.test_password
        )
    
    def test_registration_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'csrfmiddlewaretoken')
    
    def test_registration_post(self):
        test_pass = os.environ.get('TEST_PASSWORD', 'newpass123')
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': test_pass,
            'password2': test_pass
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
        self.client.login(username='testuser', password=self.test_password)
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
    
    def test_logout_functionality(self):
        self.client.login(username='testuser', password=self.test_password)
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
    
    def test_password_hashing(self):
        user = User.objects.get(username='testuser')
        self.assertNotEqual(user.password, self.test_password)
        self.assertTrue(user.password.startswith('pbkdf2_'))