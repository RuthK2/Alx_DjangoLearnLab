from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from blog.models import Post, Tag
import os

class TaggingSearchTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_password = os.environ.get('TEST_PASSWORD', 'testpass123')
        self.user = User.objects.create_user('testuser', 'test@test.com', self.test_password)
        self.post1 = Post.objects.create(title='Django Tutorial', content='Learn Django', author=self.user)
        self.post2 = Post.objects.create(title='Python Guide', content='Python basics', author=self.user)
        self.tag1 = Tag.objects.create(name='django')
        self.tag2 = Tag.objects.create(name='python')
        self.post1.tags.add(self.tag1)
        self.post2.tags.add(self.tag2)
    
    def test_search_by_title(self):
        response = self.client.get(reverse('search'), {'q': 'Django'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Django Tutorial')
    
    def test_search_by_content(self):
        response = self.client.get(reverse('search'), {'q': 'basics'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Python Guide')
    
    def test_search_by_tag(self):
        response = self.client.get(reverse('search'), {'q': 'django'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Django Tutorial')
    
    def test_search_no_results(self):
        response = self.client.get(reverse('search'), {'q': 'nonexistent'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No posts found')
    
    def test_filter_by_tag(self):
        response = self.client.get(reverse('posts-by-tag', kwargs={'tag_name': 'django'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Django Tutorial')
        self.assertNotContains(response, 'Python Guide')
    
    def test_tag_display_on_post_detail(self):
        response = self.client.get(reverse('post-detail', kwargs={'pk': self.post1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '#django')
    
    def test_tag_display_on_post_list(self):
        response = self.client.get(reverse('post-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '#django')
        self.assertContains(response, '#python')
    
    def test_tag_link_works(self):
        response = self.client.get(reverse('post-detail', kwargs={'pk': self.post1.pk}))
        self.assertContains(response, reverse('posts-by-tag', kwargs={'tag_name': 'django'}))
    
    def test_search_form_in_base(self):
        response = self.client.get(reverse('post-list'))
        self.assertContains(response, 'name="q"')
        self.assertContains(response, 'Search')
