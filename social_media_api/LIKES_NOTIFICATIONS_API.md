# Likes and Notifications API Documentation

## Overview
The Likes and Notifications system enhances user engagement by allowing users to like posts and receive real-time notifications about interactions with their content.

## Authentication
All endpoints require token authentication:
```
Authorization: Token YOUR_TOKEN_HERE
```

## Likes System

### Like a Post
**Endpoint:** `POST /api/posts/{post_id}/like/`

**Description:** Allows authenticated users to like a post. Creates a notification for the post author.

**Request:**
```http
POST /api/posts/1/like/
Authorization: Token abc123def456
Content-Type: application/json
```

**Success Response (200):**
```json
{
    "message": "Post liked"
}
```

**Error Response (400) - Already Liked:**
```json
{
    "error": "Post already liked"
}
```

### Unlike a Post
**Endpoint:** `POST /api/posts/{post_id}/unlike/`

**Description:** Removes a like from a post.

**Request:**
```http
POST /api/posts/1/unlike/
Authorization: Token abc123def456
Content-Type: application/json
```

**Success Response (200):**
```json
{
    "message": "Post unliked"
}
```

## Notifications System

### Get User Notifications
**Endpoint:** `GET /api/notifications/`

**Description:** Retrieves all notifications for the authenticated user, ordered by most recent.

**Request:**
```http
GET /api/notifications/
Authorization: Token abc123def456
```

**Success Response (200):**
```json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "actor_username": "john_doe",
            "verb": "liked your post",
            "timestamp": "2024-01-15T10:30:00Z",
            "read": false
        },
        {
            "id": 2,
            "actor_username": "jane_smith",
            "verb": "liked your post",
            "timestamp": "2024-01-15T09:15:00Z",
            "read": false
        }
    ]
}
```

### Get Single Notification
**Endpoint:** `GET /api/notifications/{notification_id}/`

**Request:**
```http
GET /api/notifications/1/
Authorization: Token abc123def456
```

**Success Response (200):**
```json
{
    "id": 1,
    "actor_username": "john_doe",
    "verb": "liked your post",
    "timestamp": "2024-01-15T10:30:00Z",
    "read": false
}
```

## User Interaction Flow

### Typical Like Workflow:
1. **User A** creates a post
2. **User B** likes the post via `POST /api/posts/{id}/like/`
3. System creates a notification for **User A**
4. **User A** checks notifications via `GET /api/notifications/`
5. **User A** sees "User B liked your post"

### Example Complete Flow:

**Step 1: User A creates post**
```http
POST /api/posts/
Authorization: Token user_a_token
{
    "title": "My awesome post",
    "content": "Check out this amazing content!"
}
```

**Step 2: User B likes the post**
```http
POST /api/posts/1/like/
Authorization: Token user_b_token
```

**Step 3: User A checks notifications**
```http
GET /api/notifications/
Authorization: Token user_a_token
```

**Response:**
```json
{
    "results": [
        {
            "id": 1,
            "actor_username": "user_b",
            "verb": "liked your post",
            "timestamp": "2024-01-15T10:30:00Z",
            "read": false
        }
    ]
}
```

## Business Benefits

### User Engagement
- **Instant Feedback:** Users receive immediate notifications when their content is liked
- **Social Validation:** Like counts provide social proof and encourage content creation
- **Activity Tracking:** Users can monitor engagement on their posts

### Platform Growth
- **Increased Retention:** Notifications bring users back to the platform
- **Content Discovery:** Popular posts (with more likes) can be promoted
- **Community Building:** Likes create connections between users

### Analytics Opportunities
- **Engagement Metrics:** Track which content performs best
- **User Behavior:** Understand user preferences through like patterns
- **Content Optimization:** Help creators improve based on like feedback

## Error Handling

### Common Error Responses:

**401 Unauthorized:**
```json
{
    "detail": "Authentication credentials were not provided."
}
```

**404 Not Found:**
```json
{
    "detail": "Not found."
}
```

**400 Bad Request:**
```json
{
    "error": "Post already liked"
}
```

## Rate Limiting
- Likes: Standard user rate limits apply
- Notifications: Read-only operations, higher limits

## Security Features
- Users can only like posts once
- Users cannot like their own posts (no self-notifications)
- Notifications are private to each user
- Token authentication required for all operations