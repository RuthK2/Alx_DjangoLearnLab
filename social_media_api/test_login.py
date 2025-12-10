#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_api.settings')
django.setup()

from django.contrib.auth import authenticate, get_user_model

User = get_user_model()

# Test authentication
print("Testing authentication...")
user = authenticate(username='testuser1', password='testpass123')
if user:
    print(f"SUCCESS: Authentication successful for {user.username}")
else:
    print("FAILED: Authentication failed")
    
    # Check if user exists
    try:
        user_obj = User.objects.get(username='testuser1')
        print(f"User exists: {user_obj.username}")
        print(f"User is active: {user_obj.is_active}")
        
        # Test password
        if user_obj.check_password('testpass123'):
            print("SUCCESS: Password is correct")
        else:
            print("FAILED: Password is incorrect")
            # Reset password
            user_obj.set_password('testpass123')
            user_obj.save()
            print("Password reset to 'testpass123'")
            
    except User.DoesNotExist:
        print("User does not exist")