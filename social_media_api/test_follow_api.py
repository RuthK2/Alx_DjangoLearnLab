#!/usr/bin/env python
"""
Test script for Follow functionality and Feed API endpoints.
Run this after starting the Django server with: python manage.py runserver

Prerequisites:
1. Have at least 2 users in the database
2. Know their usernames and passwords
3. Server running on http://127.0.0.1:8000
"""

import requests
import json

BASE_URL = 'http://127.0.0.1:8000/api'

class FollowAPITester:
    def __init__(self):
        self.tokens = {}
        
    def login_user(self, username, password):
        """Login user and store token"""
        print(f"\n🔐 Logging in user: {username}")
        response = requests.post(f"{BASE_URL}/accounts/login/", json={
            "username": username,
            "password": password
        })
        
        if response.status_code == 200:
            token = response.json().get('token')
            self.tokens[username] = token
            print(f"✅ Login successful. Token: {token[:20]}...")
            return token
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    
    def get_headers(self, username):
        """Get authorization headers for user"""
        token = self.tokens.get(username)
        if not token:
            print(f"❌ No token found for {username}")
            return {}
        return {"Authorization": f"Token {token}"}
    
    def follow_user(self, follower_username, target_user_id):
        """Test follow functionality"""
        print(f"\n👥 {follower_username} following user ID {target_user_id}")
        headers = self.get_headers(follower_username)
        
        response = requests.post(
            f"{BASE_URL}/accounts/follow/{target_user_id}/",
            headers=headers
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    
    def unfollow_user(self, follower_username, target_user_id):
        """Test unfollow functionality"""
        print(f"\n👥 {follower_username} unfollowing user ID {target_user_id}")
        headers = self.get_headers(follower_username)
        
        response = requests.post(
            f"{BASE_URL}/accounts/unfollow/{target_user_id}/",
            headers=headers
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    
    def create_post(self, username, title, content):
        """Create a test post"""
        print(f"\n📝 {username} creating post: {title}")
        headers = self.get_headers(username)
        
        response = requests.post(f"{BASE_URL}/posts/", 
            headers=headers,
            json={
                "title": title,
                "content": content
            }
        )
        
        print(f"Status: {response.status_code}")
        if response.status_code == 201:
            print("✅ Post created successfully")
            return response.json()
        else:
            print(f"❌ Post creation failed: {response.text}")
            return None
    
    def get_feed(self, username):
        """Test feed functionality"""
        print(f"\n📰 Getting feed for {username}")
        headers = self.get_headers(username)
        
        response = requests.get(f"{BASE_URL}/feed/", headers=headers)
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Feed contains {data.get('count', 0)} posts")
            for post in data.get('results', [])[:3]:  # Show first 3 posts
                print(f"  - {post.get('title')} by {post.get('author', {}).get('username')}")
            return data
        else:
            print(f"❌ Feed access failed: {response.text}")
            return None
    
    def test_self_follow_prevention(self, username, user_id):
        """Test that users cannot follow themselves"""
        print(f"\n🚫 Testing self-follow prevention for {username}")
        headers = self.get_headers(username)
        
        response = requests.post(
            f"{BASE_URL}/accounts/follow/{user_id}/",
            headers=headers
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 400:
            print("✅ Self-follow prevention working correctly")
        else:
            print("❌ Self-follow prevention failed")
    
    def test_nonexistent_user(self, username):
        """Test following non-existent user"""
        print(f"\n👻 Testing follow non-existent user (ID: 9999)")
        headers = self.get_headers(username)
        
        response = requests.post(
            f"{BASE_URL}/accounts/follow/9999/",
            headers=headers
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 404:
            print("✅ Non-existent user handling working correctly")
        else:
            print("❌ Non-existent user handling failed")

def main():
    """Main test sequence"""
    tester = FollowAPITester()
    
    print("🚀 Starting Follow API Tests")
    print("=" * 50)
    
    # Configuration - Update these with your actual users
    USER1 = "testuser"  # Update with actual username
    USER1_PASS = "testpass123"  # Update with actual password
    USER1_ID = 1  # Update with actual user ID
    
    USER2 = "john"  # Update with actual username  
    USER2_PASS = "testpass123"  # Update with actual password
    USER2_ID = 2  # Update with actual user ID
    
    try:
        # Step 1: Login users
        print("\n📋 STEP 1: User Authentication")
        token1 = tester.login_user(USER1, USER1_PASS)
        token2 = tester.login_user(USER2, USER2_PASS)
        
        if not token1 or not token2:
            print("❌ Authentication failed. Please check usernames/passwords.")
            return
        
        # Step 2: Test self-follow prevention
        print("\n📋 STEP 2: Self-Follow Prevention")
        tester.test_self_follow_prevention(USER1, USER1_ID)
        
        # Step 3: Test non-existent user
        print("\n📋 STEP 3: Non-existent User Handling")
        tester.test_nonexistent_user(USER1)
        
        # Step 4: Create posts as USER2
        print("\n📋 STEP 4: Create Test Posts")
        tester.create_post(USER2, "Hello Followers!", "This is my first post")
        tester.create_post(USER2, "Django Tutorial", "Learning Django REST framework")
        
        # Step 5: Check USER1's feed (should be empty)
        print("\n📋 STEP 5: Check Empty Feed")
        tester.get_feed(USER1)
        
        # Step 6: USER1 follows USER2
        print("\n📋 STEP 6: Follow User")
        tester.follow_user(USER1, USER2_ID)
        
        # Step 7: Check USER1's feed (should show USER2's posts)
        print("\n📋 STEP 7: Check Feed After Following")
        tester.get_feed(USER1)
        
        # Step 8: USER1 unfollows USER2
        print("\n📋 STEP 8: Unfollow User")
        tester.unfollow_user(USER1, USER2_ID)
        
        # Step 9: Check USER1's feed (should be empty again)
        print("\n📋 STEP 9: Check Feed After Unfollowing")
        tester.get_feed(USER1)
        
        print("\n🎉 All tests completed!")
        print("=" * 50)
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to Django server.")
        print("Please start the server with: python manage.py runserver")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()