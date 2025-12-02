from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

class EditProfileTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_edit_profile_get(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'csrfmiddlewaretoken')
    
    def test_edit_profile_post(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('edit_profile'), {
            'username': 'updateduser',
            'email': 'updated@example.com',
            'first_name': 'Updated',
            'last_name': 'User'
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')
        self.assertEqual(self.user.email, 'updated@example.com')