# Django REST Framework Authentication & Permission Setup

## Overview
This document explains how authentication and permissions are configured in the API project.

## 1. Settings Configuration (settings.py)

### Token Authentication Setup
```python
INSTALLED_APPS = [
    # ... other apps
    'rest_framework',
    'rest_framework.authtoken',  # Enables token authentication
    'api'
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',  # Token-based auth
        'rest_framework.authentication.SessionAuthentication',  # Session auth for admin
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',     # Limits anonymous users
        'rest_framework.throttling.UserRateThrottle'     # Limits authenticated users
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',   # Anonymous users: 100 requests per hour
        'user': '1000/hour'   # Authenticated users: 1000 requests per hour
    }
}
```

## 2. Authentication Views (urls.py)

### Token Retrieval Endpoint
```python
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('auth/token/', obtain_auth_token, name='api_token_auth'),  # Get token endpoint
    # ... other URLs
]
```

**Usage**: POST to `/api/auth/token/` with username/password to get authentication token.

## 3. Permission Classes (views.py)

### BookList View
```python
class BookList(generics.ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]  # Anyone can read, auth required to write
```

### BookViewSet
```python
class BookViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]  # Authentication required for all operations
    
    def get_permissions(self):
        if self.action == 'destroy':
            permission_classes = [IsAdminUser]  # Only admin can delete
        else:
            permission_classes = [IsAuthenticated]  # Auth required for other operations
        return [permission() for permission in permission_classes]
```

## 4. How It Works

### Getting a Token
1. POST to `/api/auth/token/` with:
   ```json
   {
       "username": "your_username",
       "password": "your_password"
   }
   ```
2. Receive token response:
   ```json
   {
       "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
   }
   ```

### Using the Token
Include in request headers:
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

### Permission Levels
- **Public**: Can read books without authentication
- **Authenticated**: Can create, read, update books
- **Admin**: Can delete books (requires superuser status)

## 5. Security Features

- **Rate Limiting**: Prevents DoS attacks
- **Token Authentication**: Secure API access
- **Permission Classes**: Role-based access control
- **CSRF Protection**: Enabled for web requests

## 6. Testing Users

- **Regular User**: `apiuser` / `testpass123`
- **Admin User**: `apiuser@example.com` / `testpass123`

Use admin user token for delete operations.