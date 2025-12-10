#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_api.settings')
django.setup()

from django.contrib.auth import get_user_model
from posts.models import Post, Comment

User = get_user_model()

# Create test users
user1, created = User.objects.get_or_create(
    username='testuser1',
    defaults={'email': 'test1@example.com'}
)
if created:
    user1.set_password('testpass123')
    user1.save()
    print(f"Created user: {user1.username}")

user2, created = User.objects.get_or_create(
    username='testuser2', 
    defaults={'email': 'test2@example.com'}
)
if created:
    user2.set_password('testpass123')
    user2.save()
    print(f"Created user: {user2.username}")

# Create test posts
post1, created = Post.objects.get_or_create(
    title='First Test Post',
    defaults={
        'content': 'This is the content of the first test post.',
        'author': user1
    }
)
if created:
    print(f"Created post: {post1.title}")

post2, created = Post.objects.get_or_create(
    title='Second Test Post',
    defaults={
        'content': 'This is the content of the second test post.',
        'author': user2
    }
)
if created:
    print(f"Created post: {post2.title}")

# Create test comments
comment1, created = Comment.objects.get_or_create(
    content='Great post!',
    defaults={
        'author': user2,
        'post': post1
    }
)
if created:
    print(f"Created comment: {comment1.content}")

comment2, created = Comment.objects.get_or_create(
    content='Thanks for sharing!',
    defaults={
        'author': user1,
        'post': post2
    }
)
if created:
    print(f"Created comment: {comment2.content}")

print("\nTest data created successfully!")
print("Test users:")
print(f"- Username: testuser1, Password: testpass123")
print(f"- Username: testuser2, Password: testpass123")