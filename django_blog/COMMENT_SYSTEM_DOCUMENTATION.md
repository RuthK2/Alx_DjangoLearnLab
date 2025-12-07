# Comment System Documentation

## Overview
The blog comment system allows authenticated users to add comments to blog posts. Comment authors can edit and delete their own comments.

## Features

### 1. Add Comments
- **Who**: Authenticated users only
- **Where**: On any blog post detail page
- **How**: Click "Add Comment" button at the bottom of the post

### 2. View Comments
- **Who**: All users (public)
- **Where**: Blog post detail page
- **Display**: Shows author, timestamp, and content

### 3. Edit Comments
- **Who**: Comment author only
- **Where**: Edit button appears next to own comments
- **How**: Click "Edit" button on your comment

### 4. Delete Comments
- **Who**: Comment author only
- **Where**: Delete button appears next to own comments
- **How**: Click "Delete" button, then confirm deletion

## User Permissions

### Public Users (Not Logged In)
- ✅ View all comments
- ❌ Cannot add comments
- ❌ Cannot edit comments
- ❌ Cannot delete comments

### Authenticated Users
- ✅ View all comments
- ✅ Add comments to any post
- ✅ Edit own comments only
- ✅ Delete own comments only
- ❌ Cannot edit others' comments
- ❌ Cannot delete others' comments

## URL Structure

| Action | URL Pattern | View |
|--------|-------------|------|
| Add Comment | `/post/<post_id>/comments/new/` | CommentCreateView |
| Edit Comment | `/comment/<comment_id>/update/` | CommentUpdateView |
| Delete Comment | `/comment/<comment_id>/delete/` | CommentDeleteView |

## Comment Model Fields

- **post**: Link to the blog post (ForeignKey)
- **author**: User who wrote the comment (ForeignKey)
- **content**: Comment text (TextField)
- **created_at**: Timestamp when created (auto-generated)
- **updated_at**: Timestamp when last modified (auto-updated)

## Usage Guide

### Adding a Comment

1. Navigate to any blog post
2. Scroll to the Comments section
3. Click "Add Comment" button
4. Enter your comment text
5. Click "Save"
6. You'll be redirected back to the post with your comment visible

### Editing Your Comment

1. Find your comment on the post
2. Click "Edit" button next to your comment
3. Modify the comment text
4. Click "Save" to update
5. Click "Cancel" to discard changes

### Deleting Your Comment

1. Find your comment on the post
2. Click "Delete" button next to your comment
3. Confirm deletion on the confirmation page
4. Click "Confirm Delete" to permanently remove
5. Click "Cancel" to keep the comment

## Security Features

### Authentication Required
- Users must be logged in to add comments
- Unauthenticated users are redirected to login page

### Authorization Checks
- Only comment authors can edit their comments
- Only comment authors can delete their comments
- Attempting to edit/delete others' comments returns 403 Forbidden

### CSRF Protection
- All comment forms include CSRF tokens
- Prevents cross-site request forgery attacks

## Comment Display

Comments are displayed in chronological order (oldest first) showing:
- Author username
- Creation timestamp
- Comment content
- Edit/Delete buttons (for comment author only)

## Technical Implementation

### Models
```python
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### Views
- **CommentCreateView**: LoginRequiredMixin, CreateView
- **CommentUpdateView**: LoginRequiredMixin, UserPassesTestMixin, UpdateView
- **CommentDeleteView**: LoginRequiredMixin, UserPassesTestMixin, DeleteView

### Forms
- **CommentForm**: ModelForm with content field and textarea widget

## Troubleshooting

### "Add Comment" button not visible
- **Solution**: Make sure you're logged in

### Cannot edit/delete a comment
- **Solution**: You can only edit/delete your own comments

### 403 Forbidden error
- **Solution**: You're trying to modify someone else's comment

### Comment not saving
- **Solution**: Check that content field is not empty

## Best Practices

### For Users
- Keep comments relevant to the post
- Be respectful in your comments
- Review before posting

### For Developers
- Always check user authentication before allowing comment operations
- Verify comment ownership before edit/delete operations
- Use Django's built-in mixins for security
- Include CSRF tokens in all forms
