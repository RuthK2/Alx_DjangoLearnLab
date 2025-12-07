# Comment System Testing Guide

## Pre-Testing Setup

### 1. Ensure Server is Running
```bash
cd c:\Users\Belle\Alx_DjangoLearnLab\django_blog
python manage.py runserver
```

### 2. Create Test Users
```bash
python manage.py shell
```
```python
from django.contrib.auth.models import User
User.objects.create_user('user1', 'user1@test.com', 'testpass123')
User.objects.create_user('user2', 'user2@test.com', 'testpass123')
exit()
```

### 3. Create Test Post
- Login as user1
- Create a blog post titled "Test Post for Comments"

## Test Cases

### Test 1: View Comments (Public Access)
**Objective**: Verify anyone can view comments

**Steps:**
1. Logout (if logged in)
2. Navigate to a blog post: `http://127.0.0.1:8000/posts/1/`
3. Scroll to Comments section

**Expected Results:**
- ✅ Comments section is visible
- ✅ Existing comments display (if any)
- ✅ "Add Comment" button is NOT visible
- ✅ Edit/Delete buttons are NOT visible

**Status:** [ ] Pass [ ] Fail

---

### Test 2: Add Comment (Authenticated User)
**Objective**: Verify authenticated users can add comments

**Steps:**
1. Login as user1
2. Navigate to a blog post
3. Click "Add Comment" button
4. Enter comment: "This is my first comment"
5. Click "Save"

**Expected Results:**
- ✅ Redirects to post detail page
- ✅ New comment appears in comments section
- ✅ Comment shows correct author (user1)
- ✅ Comment shows timestamp
- ✅ Edit/Delete buttons visible on own comment

**Status:** [ ] Pass [ ] Fail

---

### Test 3: Add Comment (Unauthenticated User)
**Objective**: Verify unauthenticated users cannot add comments

**Steps:**
1. Logout
2. Navigate to: `http://127.0.0.1:8000/post/1/comments/new/`

**Expected Results:**
- ✅ Redirects to login page
- ✅ Cannot access comment form

**Status:** [ ] Pass [ ] Fail

---

### Test 4: Edit Own Comment
**Objective**: Verify users can edit their own comments

**Steps:**
1. Login as user1
2. Navigate to post with user1's comment
3. Click "Edit" button on own comment
4. Change text to: "This is my edited comment"
5. Click "Save"

**Expected Results:**
- ✅ Redirects to post detail page
- ✅ Comment text is updated
- ✅ updated_at timestamp changes
- ✅ Author remains the same

**Status:** [ ] Pass [ ] Fail

---

### Test 5: Edit Own Comment - Cancel
**Objective**: Verify cancel button works

**Steps:**
1. Login as user1
2. Click "Edit" on own comment
3. Change text
4. Click "Cancel"

**Expected Results:**
- ✅ Returns to post detail page
- ✅ Comment text unchanged
- ✅ No changes saved

**Status:** [ ] Pass [ ] Fail

---

### Test 6: Delete Own Comment
**Objective**: Verify users can delete their own comments

**Steps:**
1. Login as user1
2. Navigate to post with user1's comment
3. Click "Delete" button on own comment
4. Review confirmation page
5. Click "Confirm Delete"

**Expected Results:**
- ✅ Shows confirmation page with comment preview
- ✅ Redirects to post detail page
- ✅ Comment is removed from display
- ✅ Comment deleted from database

**Status:** [ ] Pass [ ] Fail

---

### Test 7: Delete Own Comment - Cancel
**Objective**: Verify cancel button works on delete

**Steps:**
1. Login as user1
2. Click "Delete" on own comment
3. Click "Cancel" on confirmation page

**Expected Results:**
- ✅ Returns to post detail page
- ✅ Comment still exists
- ✅ No deletion occurred

**Status:** [ ] Pass [ ] Fail

---

### Test 8: Cannot Edit Others' Comments (UI)
**Objective**: Verify edit button doesn't show for others' comments

**Steps:**
1. Login as user1, add a comment
2. Logout, login as user2
3. Navigate to post with user1's comment

**Expected Results:**
- ✅ user1's comment is visible
- ✅ Edit button NOT visible on user1's comment
- ✅ Delete button NOT visible on user1's comment

**Status:** [ ] Pass [ ] Fail

---

### Test 9: Cannot Edit Others' Comments (Direct URL)
**Objective**: Verify authorization prevents editing others' comments

**Steps:**
1. Login as user1, create comment (note comment ID)
2. Logout, login as user2
3. Try to access: `http://127.0.0.1:8000/comment/1/update/`

**Expected Results:**
- ✅ Returns 403 Forbidden error
- ✅ Cannot access edit form
- ✅ Comment remains unchanged

**Status:** [ ] Pass [ ] Fail

---

### Test 10: Cannot Delete Others' Comments (Direct URL)
**Objective**: Verify authorization prevents deleting others' comments

**Steps:**
1. Login as user1, create comment (note comment ID)
2. Logout, login as user2
3. Try to access: `http://127.0.0.1:8000/comment/1/delete/`

**Expected Results:**
- ✅ Returns 403 Forbidden error
- ✅ Cannot access delete confirmation
- ✅ Comment remains in database

**Status:** [ ] Pass [ ] Fail

---

### Test 11: Multiple Comments on Same Post
**Objective**: Verify multiple users can comment on same post

**Steps:**
1. Login as user1, add comment "Comment from user1"
2. Logout, login as user2, add comment "Comment from user2"
3. View post as public user

**Expected Results:**
- ✅ Both comments visible
- ✅ Comments show correct authors
- ✅ Comments display in order
- ✅ Each user sees edit/delete only on own comments

**Status:** [ ] Pass [ ] Fail

---

### Test 12: Empty Comment Validation
**Objective**: Verify empty comments are rejected

**Steps:**
1. Login as user1
2. Click "Add Comment"
3. Leave content field empty
4. Click "Save"

**Expected Results:**
- ✅ Form validation error appears
- ✅ Comment not saved
- ✅ User remains on form page

**Status:** [ ] Pass [ ] Fail

---

### Test 13: CSRF Protection
**Objective**: Verify CSRF tokens are present

**Steps:**
1. Login as user1
2. Click "Add Comment"
3. Inspect form HTML

**Expected Results:**
- ✅ Form contains `csrfmiddlewaretoken` hidden input
- ✅ Token has a value

**Status:** [ ] Pass [ ] Fail

---

### Test 14: Comment Display Order
**Objective**: Verify comments display in correct order

**Steps:**
1. Login as user1
2. Add 3 comments with different timestamps
3. View post

**Expected Results:**
- ✅ Comments display in chronological order
- ✅ Oldest comment appears first
- ✅ Newest comment appears last

**Status:** [ ] Pass [ ] Fail

---

### Test 15: Updated Timestamp
**Objective**: Verify updated_at changes on edit

**Steps:**
1. Login as user1
2. Create a comment, note created_at time
3. Wait 1 minute
4. Edit the comment
5. Check database or admin panel

**Expected Results:**
- ✅ created_at remains unchanged
- ✅ updated_at reflects new time
- ✅ updated_at > created_at

**Status:** [ ] Pass [ ] Fail

---

## Database Verification Tests

### Test 16: Verify Comment in Database
```bash
python manage.py shell
```
```python
from blog.models import Comment
comments = Comment.objects.all()
print(f"Total comments: {comments.count()}")
for c in comments:
    print(f"ID: {c.id}, Author: {c.author}, Post: {c.post}")
```

**Expected Results:**
- ✅ Comments exist in database
- ✅ Correct relationships to Post and User

---

### Test 17: Cascade Deletion (Post)
```python
from blog.models import Post, Comment
post = Post.objects.first()
comment_count = post.comments.count()
post.delete()
# Check if comments deleted
```

**Expected Results:**
- ✅ Deleting post deletes associated comments
- ✅ CASCADE behavior works correctly

---

## Security Testing Checklist

- [ ] Unauthenticated users cannot add comments
- [ ] Unauthenticated users cannot edit comments
- [ ] Unauthenticated users cannot delete comments
- [ ] Users cannot edit others' comments (UI)
- [ ] Users cannot edit others' comments (direct URL)
- [ ] Users cannot delete others' comments (UI)
- [ ] Users cannot delete others' comments (direct URL)
- [ ] CSRF tokens present on all forms
- [ ] SQL injection protection (Django ORM handles this)

## Performance Testing

### Test 18: Many Comments
**Steps:**
1. Create 50+ comments on a single post
2. Load the post detail page
3. Check page load time

**Expected Results:**
- ✅ Page loads in reasonable time
- ✅ All comments display correctly
- ✅ No performance degradation

---

## Summary Report Template

**Test Date:** ___________
**Tester:** ___________
**Total Tests:** 18
**Passed:** ___________
**Failed:** ___________
**Pass Rate:** ___________%

**Critical Issues Found:**
1. 
2. 
3. 

**Minor Issues Found:**
1. 
2. 
3. 

**Recommendations:**
1. 
2. 
3. 

**Overall Status:** [ ] Ready for Production [ ] Needs Fixes
