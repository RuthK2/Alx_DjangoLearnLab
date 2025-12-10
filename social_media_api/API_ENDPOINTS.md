# API Endpoints Quick Reference

## Base URL
```
http://127.0.0.1:8000/api
```

## Authentication
All protected endpoints require:
```
Authorization: Token your_auth_token_here
```

## Endpoints Summary

### 🔐 Authentication
| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| POST | `/accounts/register/` | ❌ | Register new user |
| POST | `/accounts/login/` | ❌ | Login user |
| GET | `/accounts/profile/` | ✅ | Get user profile |

### 👥 Follow Management
| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| POST | `/accounts/follow/<user_id>/` | ✅ | Follow a user |
| POST | `/accounts/unfollow/<user_id>/` | ✅ | Unfollow a user |

### 📰 Feed
| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| GET | `/feed/` | ✅ | Get personalized feed |

### 📝 Posts
| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| GET | `/posts/` | ❌ | List all posts |
| POST | `/posts/` | ✅ | Create new post |
| GET | `/posts/<id>/` | ❌ | Get specific post |
| PUT | `/posts/<id>/` | ✅ | Update post (author only) |
| DELETE | `/posts/<id>/` | ✅ | Delete post (author only) |

### 💬 Comments
| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| GET | `/comments/` | ❌ | List all comments |
| POST | `/comments/` | ✅ | Create new comment |
| GET | `/comments/<id>/` | ❌ | Get specific comment |
| PUT | `/comments/<id>/` | ✅ | Update comment (author only) |
| DELETE | `/comments/<id>/` | ✅ | Delete comment (author only) |

## Query Parameters

### Posts & Comments
- `search`: Search in title/content
- `author`: Filter by author ID
- `ordering`: Order by field (prefix with `-` for descending)
- `page`: Page number
- `page_size`: Items per page

### Feed
- `page`: Page number
- `page_size`: Posts per page (max 100)

## Example Requests

### Register User
```bash
curl -X POST http://127.0.0.1:8000/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "newuser", "email": "user@example.com", "password": "securepass123"}'
```

### Login
```bash
curl -X POST http://127.0.0.1:8000/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "newuser", "password": "securepass123"}'
```

### Follow User
```bash
curl -X POST http://127.0.0.1:8000/api/accounts/follow/2/ \
  -H "Authorization: Token your_token_here"
```

### Get Feed
```bash
curl -X GET http://127.0.0.1:8000/api/feed/ \
  -H "Authorization: Token your_token_here"
```

### Create Post
```bash
curl -X POST http://127.0.0.1:8000/api/posts/ \
  -H "Authorization: Token your_token_here" \
  -H "Content-Type: application/json" \
  -d '{"title": "My Post", "content": "Post content here"}'
```

### Search Posts
```bash
curl -X GET "http://127.0.0.1:8000/api/posts/?search=django&ordering=-created_at"
```

## Response Formats

### Success Response (Follow)
```json
{
    "message": "You are now following john"
}
```

### Error Response (Self-follow)
```json
{
    "error": "You cannot follow yourself"
}
```

### Feed Response
```json
{
    "count": 10,
    "next": "http://127.0.0.1:8000/api/feed/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "Post Title",
            "content": "Post content...",
            "author": {
                "id": 2,
                "username": "john"
            },
            "created_at": "2024-01-15T10:30:00Z"
        }
    ]
}
```

## Testing Tools

### Python Test Script
```bash
python test_follow_api.py
```

### Manual Testing
1. Start server: `python manage.py runserver`
2. Use Postman or curl with the endpoints above
3. Follow the authentication flow first
4. Test follow → create posts → check feed → unfollow sequence