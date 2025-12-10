# Social Media API Documentation

## Overview
A Django REST API for a social media platform with user authentication, posts, comments, follow functionality, and personalized feeds.

## Features
- User registration and authentication
- Create, read, update, delete posts and comments
- Follow/unfollow users
- Personalized feed based on followed users
- Search, filtering, and pagination

## Model Changes

### CustomUser Model
The user model has been updated to support follow functionality:

```python
class CustomUser(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following')
```

**Key Changes:**
- Added `followers` field: Many-to-many relationship to self
- `symmetrical=False`: Following is not mutual by default
- `related_name='following'`: Provides reverse relationship

**Relationship Usage:**
- `user.followers.all()` - Get users who follow this user
- `user.following.all()` - Get users this user follows

## API Endpoints

### Authentication Endpoints

#### Register User
```
POST /api/accounts/register/
```
**Body:**
```json
{
    "username": "newuser",
    "email": "user@example.com",
    "password": "securepassword123"
}
```
**Response:**
```json
{
    "message": "User created successfully",
    "token": "your_auth_token_here"
}
```

#### Login
```
POST /api/accounts/login/
```
**Body:**
```json
{
    "username": "newuser",
    "password": "securepassword123"
}
```
**Response:**
```json
{
    "message": "Login successful",
    "token": "your_auth_token_here"
}
```

#### Get Profile
```
GET /api/accounts/profile/
```
**Headers:** `Authorization: Token your_auth_token_here`

### Follow Management Endpoints

#### Follow User
```
POST /api/accounts/follow/<user_id>/
```
**Headers:** `Authorization: Token your_auth_token_here`

**Example:**
```bash
POST /api/accounts/follow/2/
Authorization: Token abc123def456
```

**Success Response:**
```json
{
    "message": "You are now following john"
}
```

**Error Responses:**
- **400 Bad Request:** Self-follow attempt
```json
{
    "error": "You cannot follow yourself"
}
```
- **404 Not Found:** User doesn't exist
```json
{
    "error": "User not found"
}
```

#### Unfollow User
```
POST /api/accounts/unfollow/<user_id>/
```
**Headers:** `Authorization: Token your_auth_token_here`

**Example:**
```bash
POST /api/accounts/unfollow/2/
Authorization: Token abc123def456
```

**Success Response:**
```json
{
    "message": "You have unfollowed john"
}
```

**Error Responses:**
- **400 Bad Request:** Self-unfollow attempt
```json
{
    "error": "You cannot unfollow yourself"
}
```
- **404 Not Found:** User doesn't exist
```json
{
    "error": "User not found"
}
```

### Feed Endpoint

#### Get Personalized Feed
```
GET /api/feed/
```
**Headers:** `Authorization: Token your_auth_token_here`

**Features:**
- Shows posts only from users you follow
- Ordered by creation date (newest first)
- Paginated results (10 posts per page)
- Read-only access (no create/update/delete)

**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Posts per page (default: 10, max: 100)

**Example:**
```bash
GET /api/feed/?page=1&page_size=5
Authorization: Token abc123def456
```

**Response:**
```json
{
    "count": 25,
    "next": "http://127.0.0.1:8000/api/feed/?page=2&page_size=5",
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "Latest Post",
            "content": "This is a post from someone I follow",
            "author": {
                "id": 2,
                "username": "john"
            },
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-15T10:30:00Z"
        }
    ]
}
```

### Posts Endpoints

#### Create Post
```
POST /api/posts/
```
**Headers:** `Authorization: Token your_auth_token_here`
**Body:**
```json
{
    "title": "My New Post",
    "content": "This is the content of my post"
}
```

#### Get Posts (with filtering and search)
```
GET /api/posts/
```
**Query Parameters:**
- `search`: Search in title and content
- `author`: Filter by author ID
- `created_at`: Filter by creation date
- `ordering`: Order by fields (created_at, updated_at, title)
- `page`: Page number
- `page_size`: Posts per page

**Examples:**
```bash
# Search posts
GET /api/posts/?search=django

# Filter by author
GET /api/posts/?author=1

# Order by creation date (newest first)
GET /api/posts/?ordering=-created_at

# Combine filters
GET /api/posts/?author=1&search=tutorial&ordering=-created_at
```

## Testing with Postman

### 1. Setup
1. Start Django server: `python manage.py runserver`
2. Base URL: `http://127.0.0.1:8000`

### 2. Authentication Flow
1. Register or login to get authentication token
2. Add token to all protected endpoints: `Authorization: Token your_token`

### 3. Follow Functionality Test Sequence

**Step 1: Login as User 1**
```
POST /api/accounts/login/
{
    "username": "testuser",
    "password": "your_password"
}
```

**Step 2: Follow Another User**
```
POST /api/accounts/follow/2/
Authorization: Token user1_token
```

**Step 3: Create Posts as User 2**
```
POST /api/posts/
Authorization: Token user2_token
{
    "title": "Test Post",
    "content": "Hello followers!"
}
```

**Step 4: Check Feed as User 1**
```
GET /api/feed/
Authorization: Token user1_token
```

**Step 5: Unfollow User**
```
POST /api/accounts/unfollow/2/
Authorization: Token user1_token
```

**Step 6: Verify Feed is Empty**
```
GET /api/feed/
Authorization: Token user1_token
```

## Error Handling

### Common HTTP Status Codes
- **200 OK:** Successful GET request
- **201 Created:** Successful POST request
- **400 Bad Request:** Invalid data or self-follow attempt
- **401 Unauthorized:** Missing or invalid authentication
- **404 Not Found:** Resource doesn't exist
- **500 Internal Server Error:** Server error

### Authentication Errors
All protected endpoints require authentication:
```json
{
    "detail": "Authentication credentials were not provided."
}
```

## Security Features
- Token-based authentication
- Permission-based access control
- Self-follow/unfollow prevention
- User isolation (users can only modify their own content)

## Database Relationships
```
CustomUser
├── followers (ManyToMany to self)
├── following (reverse relation)
├── authored_posts (reverse relation to Post)
└── authored_comments (reverse relation to Comment)

Post
├── author (ForeignKey to CustomUser)
└── comments (reverse relation)

Comment
├── author (ForeignKey to CustomUser)
└── post (ForeignKey to Post)
```

## Installation & Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Run migrations: `python manage.py migrate`
3. Create superuser: `python manage.py createsuperuser`
4. Start server: `python manage.py runserver`

## API Testing Script
Use the provided `test_api.py` script for basic endpoint testing:
```bash
python test_api.py
```