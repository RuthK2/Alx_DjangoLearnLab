#!/usr/bin/env python
"""
Simple script to test the Posts API endpoints manually.
Run this after starting the Django server with: python manage.py runserver
"""

import requests
import json

BASE_URL = 'http://127.0.0.1:8000'

def test_endpoints():
    print("Testing Posts API Endpoints...")
    
    # Test GET posts (should work without authentication)
    print("\n1. Testing GET /posts/")
    response = requests.get(f"{BASE_URL}/posts/")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
    
    # Test GET comments (should work without authentication)
    print("\n2. Testing GET /comments/")
    response = requests.get(f"{BASE_URL}/comments/")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
    
    # Test search functionality
    print("\n3. Testing search functionality")
    response = requests.get(f"{BASE_URL}/posts/?search=test")
    print(f"Search Status: {response.status_code}")
    
    # Test filtering
    print("\n4. Testing filtering")
    response = requests.get(f"{BASE_URL}/posts/?author=1")
    print(f"Filter Status: {response.status_code}")
    
    # Test pagination
    print("\n5. Testing pagination")
    response = requests.get(f"{BASE_URL}/posts/?page=1&page_size=5")
    print(f"Pagination Status: {response.status_code}")
    
    print("\nAPI endpoints are accessible!")
    print("Note: POST, PUT, DELETE operations require authentication")

if __name__ == "__main__":
    try:
        test_endpoints()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to Django server.")
        print("Please start the server with: python manage.py runserver")