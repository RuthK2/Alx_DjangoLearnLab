from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from blog.models import Post, Comment
import os

class CommentTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_password = os.environ.get('TEST_PASSWORD', 'testpass123')
        self.user1 = User.objects.create_user('user1', 'user1@test.com', self.test_password)
        self.user2 = User.objects.create_user('user2', 'user2@test.com', self.test_password)
        self.post = Post.objects.create(title='Test Post', content='Test Content', author=self.user1)
    
    def test_view_comments_public(self):
        response = self.client.get(reverse('post-detail', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Comments')
    
    def test_add_comment_authenticated(self):
        self.client.login(username='user1', password=self.test_password)
        response = self.client.post(reverse('comment-create', kwargs={'pk': self.post.pk}), {
            'content': 'This is my first comment'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.filter(content='This is my first comment').exists())
    
    def test_add_comment_unauthenticated(self):
        response = self.client.get(reverse('comment-create', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)
    
    def test_edit_own_comment(self):
        self.client.login(username='user1', password=self.test_password)
        comment = Comment.objects.create(post=self.post, author=self.user1, content='Original')
        response = self.client.post(reverse('comment-update', kwargs={'pk': comment.pk}), {
            'content': 'Edited comment'
        })
        self.assertEqual(response.status_code, 302)
        comment.refresh_from_db()
        self.assertEqual(comment.content, 'Edited comment')
    
    def test_cannot_edit_others_comment(self):
        comment = Comment.objects.create(post=self.post, author=self.user1, content='User1 comment')
        self.client.login(username='user2', password=self.test_password)
        response = self.client.get(reverse('comment-update', kwargs={'pk': comment.pk}))
        self.assertEqual(response.status_code, 403)
    
    def test_delete_own_comment(self):
        self.client.login(username='user1', password=self.test_password)
        comment = Comment.objects.create(post=self.post, author=self.user1, content='To delete')
        response = self.client.post(reverse('comment-delete', kwargs={'pk': comment.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Comment.objects.filter(pk=comment.pk).exists())
    
    def test_cannot_delete_others_comment(self):
        comment = Comment.objects.create(post=self.post, author=self.user1, content='User1 comment')
        self.client.login(username='user2', password=self.test_password)
        response = self.client.get(reverse('comment-delete', kwargs={'pk': comment.pk}))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Comment.objects.filter(pk=comment.pk).exists())
    
    def test_multiple_comments(self):
        self.client.login(username='user1', password=self.test_password)
        Comment.objects.create(post=self.post, author=self.user1, content='Comment 1')
        self.client.login(username='user2', password=self.test_password)
        Comment.objects.create(post=self.post, author=self.user2, content='Comment 2')
        response = self.client.get(reverse('post-detail', kwargs={'pk': self.post.pk}))
        self.assertContains(response, 'Comment 1')
        self.assertContains(response, 'Comment 2')
    
    def test_comment_author_display(self):
        comment = Comment.objects.create(post=self.post, author=self.user1, content='Test')
        response = self.client.get(reverse('post-detail', kwargs={'pk': self.post.pk}))
        self.assertContains(response, 'user1')
    
    def test_csrf_token_in_form(self):
        self.client.login(username='user1', password=self.test_password)
        response = self.client.get(reverse('comment-create', kwargs={'pk': self.post.pk}))
        self.assertContains(response, 'csrfmiddlewaretoken')
