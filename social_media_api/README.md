# Social Media API

A Django REST Framework-based social media API with user authentication and profile management.

## Setup Process

### 1. Install Dependencies

```bash
pip install django djangorestframework
```

### 2. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Start Development Server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

## API Endpoints

### Base URL
All endpoints are prefixed with `/api/`

### Authentication Endpoints

#### 1. Register User
- **URL**: `/api/register/`
- **Method**: `POST`
- **Auth Required**: No
- **Request Body**:
```json
{
    "username": "john",
    "email": "john@example.com",
    "password": "securepass123"
}
```
- **Success Response** (201):
```json
{
    "message": "User created successfully",
    "token": "abc123def456..."
}
```

#### 2. Login
- **URL**: `/api/login/`
- **Method**: `POST`
- **Auth Required**: No
- **Request Body**:
```json
{
    "username": "john",
    "password": "securepass123"
}
```
- **Success Response** (200):
```json
{
    "message": "Login successful",
    "token": "abc123def456..."
}
```

#### 3. Get Profile
- **URL**: `/api/profile/`
- **Method**: `GET`
- **Auth Required**: Yes
- **Headers**: `Authorization: Token YOUR_TOKEN_HERE`
- **Success Response** (200):
```json
{
    "id": 1,
    "username": "john",
    "email": "john@example.com",
    "first_name": "",
    "last_name": "",
    "bio": "",
    "profile_picture": null,
    "followers": []
}
```

## How to Register and Authenticate Users

### Using Postman

#### Register a New User:
1. Create a POST request to `http://127.0.0.1:8000/api/register/`
2. Set header: `Content-Type: application/json`
3. Add JSON body with username, email, and password
4. Send request and save the returned token

#### Login:
1. Create a POST request to `http://127.0.0.1:8000/api/login/`
2. Set header: `Content-Type: application/json`
3. Add JSON body with username and password
4. Send request and save the returned token

#### Access Protected Endpoints:
1. Add header: `Authorization: Token YOUR_TOKEN_HERE`
2. Make requests to protected endpoints like `/api/profile/`

### Using cURL

```bash
# Register
curl -X POST http://127.0.0.1:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"john","email":"john@example.com","password":"securepass123"}'

# Login
curl -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"john","password":"securepass123"}'

# Get Profile
curl -X GET http://127.0.0.1:8000/api/profile/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

## User Model Overview

### CustomUser Model
Extends Django's `AbstractUser` with additional fields:

**Fields:**
- `username` (inherited) - Unique username for login
- `email` (inherited) - User's email address
- `password` (inherited) - Hashed password
- `first_name` (inherited) - User's first name
- `last_name` (inherited) - User's last name
- `bio` - Text field for user biography (max 500 characters, optional)
- `profile_picture` - Image field for profile photo (optional)
- `followers` - ManyToMany relationship to self for follower system (non-symmetrical)

**Key Features:**
- Token-based authentication using Django REST Framework's TokenAuthentication
- Secure password hashing
- Support for social media features (bio, profile picture, followers)
- Extensible for additional social media functionality

## Project Structure

```
social_media_api/
├── accounts/
│   ├── models.py          # CustomUser model
│   ├── serializers.py     # DRF serializers
│   ├── views.py           # API views
│   └── urls.py            # App URL patterns
├── social_media_api/
│   ├── settings.py        # Project settings
│   └── urls.py            # Main URL configuration
└── manage.py
```

## Security Notes

- Passwords are automatically hashed using Django's password hashers
- Token authentication is required for protected endpoints
- CSRF protection is enabled
- Change `SECRET_KEY` and set `DEBUG = False` in production
