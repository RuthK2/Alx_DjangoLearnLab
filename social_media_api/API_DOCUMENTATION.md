# Social Media API Documentation

## Base URL
```
http://127.0.0.1:8000/api
```

## Authentication
This API uses Token-based authentication. Include the token in the Authorization header:
```
Authorization: Token YOUR_TOKEN_HERE
```

---

## Authentication Endpoints

### Register User
**POST** `/register/`

**Request:**
```json
{
    "username": "newuser",
    "email": "user@example.com",
    "password": "securepassword123"
}
```

**Response (201 Created):**
```json
{
    "message": "User created successfully",
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

### Login
**POST** `/login/`

**Request:**
```json
{
    "username": "testuser1",
    "password": "testpass123"
}
```

**Response (200 OK):**
```json
{
    "message": "Login successful",
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

---

## Posts Endpoints

### List All Posts
**GET** `/posts/`

**Query Parameters:**
- `page` - Page number (default: 1)
- `page_size` - Items per page (default: 10, max: 100)
- `search` - Search in title and content
- `author` - Filter by author ID
- `ordering` - Order by: `created_at`, `-created_at`, `updated_at`, `-updated_at`, `title`, `-title`

**Example Request:**
```
GET /posts/?search=django&page=1&page_size=5&ordering=-created_at
```

**Response (200 OK):**
```json
{
    "count": 15,
    "next": "http://127.0.0.1:8000/api/posts/?page=2&page_size=5",
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "First Test Post",
            "content": "This is the content of the first test post.",
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-15T10:30:00Z",
            "author": "testuser1"
        },
        {
            "id": 2,
            "title": "Second Test Post",
            "content": "This is the content of the second test post.",
            "created_at": "2024-01-15T09:15:00Z",
            "updated_at": "2024-01-15T09:15:00Z",
            "author": "testuser2"
        }
    ]
}
```

### Get Single Post
**GET** `/posts/{id}/`

**Response (200 OK):**
```json
{
    "id": 1,
    "title": "First Test Post",
    "content": "This is the content of the first test post.",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z",
    "author": "testuser1"
}
```

### Create Post
**POST** `/posts/`
*Requires Authentication*

**Request:**
```json
{
    "title": "My New Post",
    "content": "This is the content of my new post."
}
```

**Response (201 Created):**
```json
{
    "id": 3,
    "title": "My New Post",
    "content": "This is the content of my new post.",
    "created_at": "2024-01-15T11:00:00Z",
    "updated_at": "2024-01-15T11:00:00Z",
    "author": "testuser1"
}
```

### Update Post
**PUT** `/posts/{id}/`
*Requires Authentication - Can only update own posts*

**Request:**
```json
{
    "title": "Updated Post Title",
    "content": "Updated post content."
}
```

**Response (200 OK):**
```json
{
    "id": 3,
    "title": "Updated Post Title",
    "content": "Updated post content.",
    "created_at": "2024-01-15T11:00:00Z",
    "updated_at": "2024-01-15T11:30:00Z",
    "author": "testuser1"
}
```

**Error Response (404 Not Found) - Trying to update another user's post:**
```json
{
    "detail": "No Post matches the given query."
}
```

### Partial Update Post
**PATCH** `/posts/{id}/`
*Requires Authentication - Can only update own posts*

**Request:**
```json
{
    "title": "Only updating the title"
}
```

**Response (200 OK):**
```json
{
    "id": 3,
    "title": "Only updating the title",
    "content": "Original content remains unchanged.",
    "created_at": "2024-01-15T11:00:00Z",
    "updated_at": "2024-01-15T11:45:00Z",
    "author": "testuser1"
}
```

### Delete Post
**DELETE** `/posts/{id}/`
*Requires Authentication - Can only delete own posts*

**Response (204 No Content)**

**Error Response (404 Not Found) - Trying to delete another user's post:**
```json
{
    "detail": "No Post matches the given query."
}
```

---

## Comments Endpoints

### List All Comments
**GET** `/comments/`

**Query Parameters:**
- `page` - Page number (default: 1)
- `page_size` - Items per page (default: 10, max: 100)
- `search` - Search in content
- `post` - Filter by post ID
- `author` - Filter by author ID
- `ordering` - Order by: `created_at`, `-created_at`, `updated_at`, `-updated_at`

**Example Request:**
```
GET /comments/?post=1&ordering=-created_at
```

**Response (200 OK):**
```json
{
    "count": 5,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "content": "Great post!",
            "created_at": "2024-01-15T10:45:00Z",
            "updated_at": "2024-01-15T10:45:00Z",
            "author": "testuser2",
            "post": 1
        },
        {
            "id": 2,
            "content": "Thanks for sharing!",
            "created_at": "2024-01-15T10:40:00Z",
            "updated_at": "2024-01-15T10:40:00Z",
            "author": "testuser1",
            "post": 1
        }
    ]
}
```

### Get Single Comment
**GET** `/comments/{id}/`

**Response (200 OK):**
```json
{
    "id": 1,
    "content": "Great post!",
    "created_at": "2024-01-15T10:45:00Z",
    "updated_at": "2024-01-15T10:45:00Z",
    "author": "testuser2",
    "post": 1
}
```

### Create Comment
**POST** `/comments/`
*Requires Authentication*

**Request:**
```json
{
    "content": "This is my comment on the post!",
    "post": 1
}
```

**Response (201 Created):**
```json
{
    "id": 3,
    "content": "This is my comment on the post!",
    "created_at": "2024-01-15T12:00:00Z",
    "updated_at": "2024-01-15T12:00:00Z",
    "author": "testuser1",
    "post": 1
}
```

### Update Comment
**PUT** `/comments/{id}/`
*Requires Authentication - Can only update own comments*

**Request:**
```json
{
    "content": "Updated comment content",
    "post": 1
}
```

**Response (200 OK):**
```json
{
    "id": 3,
    "content": "Updated comment content",
    "created_at": "2024-01-15T12:00:00Z",
    "updated_at": "2024-01-15T12:15:00Z",
    "author": "testuser1",
    "post": 1
}
```

### Partial Update Comment
**PATCH** `/comments/{id}/`
*Requires Authentication - Can only update own comments*

**Request:**
```json
{
    "content": "Only updating the content"
}
```

**Response (200 OK):**
```json
{
    "id": 3,
    "content": "Only updating the content",
    "created_at": "2024-01-15T12:00:00Z",
    "updated_at": "2024-01-15T12:30:00Z",
    "author": "testuser1",
    "post": 1
}
```

### Delete Comment
**DELETE** `/comments/{id}/`
*Requires Authentication - Can only delete own comments*

**Response (204 No Content)**

---

## Error Responses

### 400 Bad Request
```json
{
    "title": ["This field is required."],
    "content": ["This field may not be blank."]
}
```

### 401 Unauthorized
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
    "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
    "detail": "No Post matches the given query."
}
```

### 405 Method Not Allowed
```json
{
    "detail": "Method \"POST\" not allowed."
}
```

---

## Usage Examples

### Complete Workflow Example

1. **Register/Login:**
```bash
curl -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser1", "password": "testpass123"}'
```

2. **Create a Post:**
```bash
curl -X POST http://127.0.0.1:8000/api/posts/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "My API Post", "content": "Created via API"}'
```

3. **Add a Comment:**
```bash
curl -X POST http://127.0.0.1:8000/api/comments/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content": "Great post!", "post": 1}'
```

4. **Search Posts:**
```bash
curl "http://127.0.0.1:8000/api/posts/?search=API&ordering=-created_at"
```

5. **Filter Comments by Post:**
```bash
curl "http://127.0.0.1:8000/api/comments/?post=1"
```

---

## Rate Limiting
- Anonymous users: 100 requests/day
- Authenticated users: 1000 requests/day

## Pagination
All list endpoints support pagination with `page` and `page_size` parameters. Maximum page size is 100.

## Permissions Summary
- **GET requests**: No authentication required
- **POST/PUT/PATCH/DELETE**: Authentication required
- **Update/Delete**: Users can only modify their own posts and comments