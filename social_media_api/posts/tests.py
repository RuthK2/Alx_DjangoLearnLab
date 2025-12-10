from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Post, Comment

User = get_user_model()


class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user
        )

    def test_post_creation(self):
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.author, self.user)
        self.assertTrue(self.post.created_at)
        self.assertTrue(self.post.updated_at)

    def test_post_str(self):
        self.assertEqual(str(self.post), 'Test Post')


class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.post = Post.objects.create(title='Test Post', content='Test content', author=self.user)
        self.comment = Comment.objects.create(
            content='Test comment',
            author=self.user,
            post=self.post
        )

    def test_comment_creation(self):
        self.assertEqual(self.comment.content, 'Test comment')
        self.assertEqual(self.comment.author, self.user)
        self.assertEqual(self.comment.post, self.post)

    def test_comment_str(self):
        expected = f"Comment by {self.user.username} on {self.post.title}"
        self.assertEqual(str(self.comment), expected)


class PostAPITest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass1')
        self.user2 = User.objects.create_user(username='user2', password='pass2')
        self.post = Post.objects.create(title='Test Post', content='Test content', author=self.user1)

    def test_get_posts_list(self):
        url = reverse('post-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_post_authenticated(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('post-list')
        data = {'title': 'New Post', 'content': 'New content'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)

    def test_create_post_unauthenticated(self):
        url = reverse('post-list')
        data = {'title': 'New Post', 'content': 'New content'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_own_post(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('post-detail', kwargs={'pk': self.post.pk})
        data = {'title': 'Updated Post', 'content': 'Updated content'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_other_user_post(self):
        self.client.force_authenticate(user=self.user2)
        url = reverse('post-detail', kwargs={'pk': self.post.pk})
        data = {'title': 'Updated Post', 'content': 'Updated content'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_own_post(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('post-detail', kwargs={'pk': self.post.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_search_posts(self):
        url = reverse('post-list')
        response = self.client.get(url, {'search': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_filter_posts_by_author(self):
        url = reverse('post-list')
        response = self.client.get(url, {'author': self.user1.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_pagination(self):
        url = reverse('post-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertIn('count', response.data)


class CommentAPITest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass1')
        self.user2 = User.objects.create_user(username='user2', password='pass2')
        self.post = Post.objects.create(title='Test Post', content='Test content', author=self.user1)
        self.comment = Comment.objects.create(content='Test comment', author=self.user1, post=self.post)

    def test_get_comments_list(self):
        url = reverse('comment-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_comment_authenticated(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('comment-list')
        data = {'content': 'New comment', 'post': self.post.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_comment_unauthenticated(self):
        url = reverse('comment-list')
        data = {'content': 'New comment', 'post': self.post.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_own_comment(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('comment-detail', kwargs={'pk': self.comment.pk})
        data = {'content': 'Updated comment', 'post': self.post.pk}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_other_user_comment(self):
        self.client.force_authenticate(user=self.user2)
        url = reverse('comment-detail', kwargs={'pk': self.comment.pk})
        data = {'content': 'Updated comment', 'post': self.post.pk}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_filter_comments_by_post(self):
        url = reverse('comment-list')
        response = self.client.get(url, {'post': self.post.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_search_comments(self):
        url = reverse('comment-list')
        response = self.client.get(url, {'search': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)