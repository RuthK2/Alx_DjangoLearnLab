from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import Book, Author

class BookAPITestCase(APITestCase):
    def setUp(self):
        """Set up test data and authentication"""
        # Create test user and token
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        
        # Create test author
        self.author = Author.objects.create(name='Test Author')
        
        # Create test books
        self.book1 = Book.objects.create(
            title='Test Book 1',
            publication_year=2020,
            author=self.author
        )
        self.book2 = Book.objects.create(
            title='Another Book',
            publication_year=2021,
            author=self.author
        )
        
        # API client
        self.client = APIClient()
    
    def test_book_list_unauthenticated(self):
        """Test that unauthenticated users can view book list"""
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_book_detail_unauthenticated(self):
        """Test that unauthenticated users can view book details"""
        url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Book 1')
    
    def test_book_create_authenticated(self):
        """Test creating a book with authentication"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse('book-create')
        data = {
            'title': 'New Book',
            'publication_year': 2022,
            'author': self.author.pk
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
    
    def test_book_create_with_login(self):
        """Test creating a book using session login"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('book-create')
        data = {
            'title': 'Login Book',
            'publication_year': 2022,
            'author': self.author.pk
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_book_create_unauthenticated(self):
        """Test that unauthenticated users cannot create books"""
        url = reverse('book-create')
        data = {
            'title': 'New Book',
            'publication_year': 2022,
            'author': self.author.pk
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_book_update_authenticated(self):
        """Test updating a book with authentication"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse('book-update', kwargs={'pk': self.book1.pk})
        data = {
            'title': 'Updated Book Title',
            'publication_year': 2023,
            'author': self.author.pk
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Book Title')
    
    def test_book_update_unauthenticated(self):
        """Test that unauthenticated users cannot update books"""
        url = reverse('book-update', kwargs={'pk': self.book1.pk})
        data = {'title': 'Updated Title'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_book_delete_authenticated(self):
        """Test deleting a book with authentication"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse('book-delete', kwargs={'pk': self.book1.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)
    
    def test_book_delete_unauthenticated(self):
        """Test that unauthenticated users cannot delete books"""
        url = reverse('book-delete', kwargs={'pk': self.book1.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_book_filtering_by_title(self):
        """Test filtering books by title"""
        url = reverse('book-list')
        response = self.client.get(url, {'title': 'Test Book 1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Book 1')
    
    def test_book_filtering_by_author(self):
        """Test filtering books by author name"""
        url = reverse('book-list')
        response = self.client.get(url, {'author__name': 'Test Author'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_book_filtering_by_publication_year(self):
        """Test filtering books by publication year"""
        url = reverse('book-list')
        response = self.client.get(url, {'publication_year': 2020})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['publication_year'], 2020)
    
    def test_book_search_by_title(self):
        """Test searching books by title"""
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'Test Book 1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_book_search_by_author_name(self):
        """Test searching books by author name"""
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'Test Author'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_book_ordering_by_title(self):
        """Test ordering books by title"""
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': 'title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, ['Another Book', 'Test Book 1'])
    
    def test_book_ordering_by_publication_year_desc(self):
        """Test ordering books by publication year descending"""
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': '-publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, [2021, 2020])
    
    def test_book_validation_future_year(self):
        """Test validation prevents future publication years"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse('book-create')
        data = {
            'title': 'Future Book',
            'publication_year': 2030,
            'author': self.author.pk
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_book_validation_invalid_year(self):
        """Test validation prevents invalid publication years"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse('book-create')
        data = {
            'title': 'Ancient Book',
            'publication_year': 500,
            'author': self.author.pk
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)