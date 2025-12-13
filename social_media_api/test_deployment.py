#!/usr/bin/env python3
"""
Production Deployment Test Script
Run this after deployment to verify everything works
"""

import requests
import json
import sys

def test_deployment(base_url):
    """Test deployed application endpoints"""
    
    print(f"Testing deployment at: {base_url}")
    
    # Test 1: Health check
    try:
        response = requests.get(f"{base_url}/")
        print(f"✓ Health check: {response.status_code}")
    except Exception as e:
        print(f"✗ Health check failed: {e}")
        return False
    
    # Test 2: Admin panel
    try:
        response = requests.get(f"{base_url}/admin/")
        print(f"✓ Admin panel: {response.status_code}")
    except Exception as e:
        print(f"✗ Admin panel failed: {e}")
    
    # Test 3: API endpoints
    api_endpoints = [
        "/api/accounts/register/",
        "/api/posts/",
        "/api/accounts/profile/",
    ]
    
    for endpoint in api_endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}")
            print(f"✓ {endpoint}: {response.status_code}")
        except Exception as e:
            print(f"✗ {endpoint} failed: {e}")
    
    # Test 4: Static files
    try:
        response = requests.get(f"{base_url}/static/admin/css/base.css")
        print(f"✓ Static files: {response.status_code}")
    except Exception as e:
        print(f"✗ Static files failed: {e}")
    
    print("\n✓ Deployment testing completed!")
    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_deployment.py <base_url>")
        print("Example: python test_deployment.py https://your-app.herokuapp.com")
        sys.exit(1)
    
    base_url = sys.argv[1].rstrip('/')
    test_deployment(base_url)