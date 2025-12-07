# Blog Post Management - CRUD Operations Documentation

## Overview
This document describes the comprehensive blog post management system with full CRUD (Create, Read, Update, Delete) operations.

## Features

### 1. List All Posts (Read)
- **URL**: `/posts/`
- **View**: `PostListView` (ListView)
- **Template**: `post_list.html`
- **Access**: Public (all users)
- **Description**: Displays all blog posts ordered by published date (newest first)

### 2. View Post Details (Read)
- **URL**: `/posts/<int:pk>/`
- **View**: `PostDetailView` (DetailView)
- **Template**: `post_detail.html`
- **Access**: Public (all users)
- **Description**: Shows full content of a single blog post with author and date

### 3. Create New Post (Create)
- **URL**: `/posts/new/`
- **View**: `PostCreateView` (CreateView)
- **Template**: `post_form.html`
- **Access**: Authenticated users only (LoginRequiredMixin)
- **Description**: Allows logged-in users to create new blog posts
- **Form Fields**: title, content
- **Auto-set**: author (from logged-in user), published_date (auto_now_add)

### 4. Edit Post (Update)
- **URL**: `/posts/<int:pk>/edit/`
- **View**: `PostUpdateView` (UpdateView)
- **Template**: `post_form.html`
- **Access**: Post author only (LoginRequiredMixin + UserPassesTestMixin)
- **Description**: Allows post authors to edit their own posts
- **Form Fields**: title, content

### 5. Delete Post (Delete)
- **URL**: `/posts/<int:pk>/delete/`
- **View**: `PostDeleteView` (DeleteView)
- **Template**: `post_confirm_delete.html`
- **Access**: Post author only (LoginRequiredMixin + UserPassesTestMixin)
- **Description**: Allows post authors to delete their own posts with confirmation

## Permissions & Security

### Authentication
- **LoginRequiredMixin**: Ensures only authenticated users can create posts
- Redirects to login page if user is not authenticated

### Authorization
- **UserPassesTestMixin**: Ensures only post authors can edit/delete their posts
- `test_func()` method checks if `request.user == post.author`
- Returns 403 Forbidden if user is not the author

### Access Control Summary
| Operation | Public | Authenticated | Author Only |
|-----------|--------|---------------|-------------|
| List      | ✓      | ✓             | ✓           |
| Detail    | ✓      | ✓             | ✓           |
| Create    | ✗      | ✓             | ✓           |
| Update    | ✗      | ✗             | ✓           |
| Delete    | ✗      | ✗             | ✓           |

## Models

### Post Model
```python
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
```

## Forms

### PostForm
- **Type**: ModelForm
- **Fields**: title, content
- **Validation**: Django's built-in validation
- **Author**: Automatically set in view's form_valid() method

## Templates

### post_list.html
- Displays all posts with title, snippet, author, and date
- Links to individual post details
- "Create New Post" button for authenticated users

### post_detail.html
- Shows full post content
- Edit/Delete buttons visible only to post author
- Back to posts list link

### post_form.html
- Reusable for both create and edit operations
- Dynamic title based on operation
- CSRF protection included
- Cancel button with context-aware redirect

### post_confirm_delete.html
- Confirmation page before deletion
- Shows post title
- Cancel option to return to post detail

## Testing Guidelines

### Functionality Tests
1. **List View**: Verify all posts display correctly
2. **Detail View**: Check individual post displays with correct data
3. **Create**: Test post creation by authenticated users
4. **Update**: Verify only authors can edit their posts
5. **Delete**: Confirm only authors can delete their posts

### Security Tests
1. **Authentication**: Unauthenticated users cannot create posts
2. **Authorization**: Users cannot edit/delete others' posts
3. **CSRF**: All forms include CSRF tokens
4. **URL Access**: Direct URL access respects permissions

### Navigation Tests
1. All links work correctly
2. Success redirects go to appropriate pages
3. Cancel buttons return to correct locations

## Usage Examples

### Creating a Post
1. User must be logged in
2. Navigate to `/posts/new/` or click "Create New Post"
3. Fill in title and content
4. Click "Save"
5. Redirected to new post detail page

### Editing a Post
1. User must be the post author
2. View post detail page
3. Click "Edit" button
4. Modify title/content
5. Click "Save"
6. Redirected to updated post detail page

### Deleting a Post
1. User must be the post author
2. View post detail page
3. Click "Delete" button
4. Confirm deletion
5. Redirected to posts list

## Code Structure

### views.py
- Class-based views for all CRUD operations
- Mixins for authentication and authorization
- Success URL configuration

### urls.py
- RESTful URL patterns
- Descriptive URL names for reverse lookups

### forms.py
- PostForm with title and content fields
- ModelForm for automatic validation

## Notes
- All views use Django's class-based views for consistency
- Author is automatically set from logged-in user
- Published date is automatically set on creation
- Edit/Delete operations include permission checks
- All forms include CSRF protection
