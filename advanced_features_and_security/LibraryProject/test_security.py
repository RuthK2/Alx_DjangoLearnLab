#!/usr/bin/env python
"""
Security Configuration Test Script
Tests HTTPS and security header configurations
"""

import os
import sys
import django
from django.conf import settings
from django.test import TestCase, Client
from django.test.utils import override_settings

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

def test_security_settings():
    """Test security settings configuration"""
    print("=== SECURITY SETTINGS TEST ===")
    
    # Test DEBUG-dependent settings
    debug_mode = settings.DEBUG
    print(f"DEBUG Mode: {debug_mode}")
    
    # HTTPS Settings
    print(f"SECURE_SSL_REDIRECT: {settings.SECURE_SSL_REDIRECT}")
    print(f"SECURE_HSTS_SECONDS: {settings.SECURE_HSTS_SECONDS}")
    print(f"SECURE_HSTS_INCLUDE_SUBDOMAINS: {settings.SECURE_HSTS_INCLUDE_SUBDOMAINS}")
    print(f"SECURE_HSTS_PRELOAD: {settings.SECURE_HSTS_PRELOAD}")
    
    # Cookie Settings
    print(f"SESSION_COOKIE_SECURE: {settings.SESSION_COOKIE_SECURE}")
    print(f"CSRF_COOKIE_SECURE: {settings.CSRF_COOKIE_SECURE}")
    print(f"SESSION_COOKIE_HTTPONLY: {settings.SESSION_COOKIE_HTTPONLY}")
    print(f"CSRF_COOKIE_HTTPONLY: {settings.CSRF_COOKIE_HTTPONLY}")
    
    # Security Headers
    print(f"X_FRAME_OPTIONS: {settings.X_FRAME_OPTIONS}")
    print(f"SECURE_CONTENT_TYPE_NOSNIFF: {settings.SECURE_CONTENT_TYPE_NOSNIFF}")
    print(f"SECURE_BROWSER_XSS_FILTER: {settings.SECURE_BROWSER_XSS_FILTER}")
    print(f"SECURE_PROXY_SSL_HEADER: {settings.SECURE_PROXY_SSL_HEADER}")

@override_settings(DEBUG=False)
def test_production_mode():
    """Test security settings in production mode"""
    print("\n=== PRODUCTION MODE TEST ===")
    
    client = Client()
    
    # Test HTTP redirect (should redirect to HTTPS in production)
    response = client.get('/', HTTP_HOST='testserver')
    print(f"HTTP Response Status: {response.status_code}")
    
    # Test security headers
    response = client.get('/', secure=True, HTTP_HOST='testserver')
    headers = response.headers if hasattr(response, 'headers') else {}
    
    print("Security Headers:")
    print(f"  X-Frame-Options: {headers.get('X-Frame-Options', 'Not Set')}")
    print(f"  X-Content-Type-Options: {headers.get('X-Content-Type-Options', 'Not Set')}")
    print(f"  X-XSS-Protection: {headers.get('X-XSS-Protection', 'Not Set')}")
    print(f"  Strict-Transport-Security: {headers.get('Strict-Transport-Security', 'Not Set')}")

def run_django_check():
    """Run Django's built-in security check"""
    print("\n=== DJANGO SECURITY CHECK ===")
    from django.core.management import execute_from_command_line
    
    try:
        execute_from_command_line(['manage.py', 'check', '--deploy'])
        print("✓ Django security check passed")
    except SystemExit as e:
        if e.code == 0:
            print("✓ Django security check passed")
        else:
            print("✗ Django security check failed")

if __name__ == '__main__':
    test_security_settings()
    test_production_mode()
    run_django_check()