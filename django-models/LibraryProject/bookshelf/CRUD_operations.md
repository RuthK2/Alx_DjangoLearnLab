# CRUD Operations Documentation

This document contains all CRUD (Create, Read, Update, Delete) operations performed on the Book model in Django shell.

## Model Definition
```python
# bookshelf/models.py
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()
    
    def __str__(self):
        return f"{self.title}, {self.author}, {self.publication_year} "
```

## CREATE Operations

### Create Book Instance
```python
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
print(book)
```
**Output:**
```
1984, George Orwell, 1949 
```

### Alternative Create Method
```python
book2 = Book(title="Animal Farm", author="George Orwell", publication_year=1945)
book2.save()
print(book2)
```
**Output:**
```
Animal Farm, George Orwell, 1945 
```

## READ (Retrieve) Operations

### Get All Books
```python
books = Book.objects.all()
print(books)
```
**Output:**
```
<QuerySet [<Book: 1984, George Orwell, 1949 >, <Book: Animal Farm, George Orwell, 1945 >]>
```

### Get Specific Book by Title
```python
book = Book.objects.get(title="1984")
print(book)
```
**Output:**
```
1984, George Orwell, 1949 
```

### Filter Books by Author
```python
orwell_books = Book.objects.filter(author="George Orwell")
print(orwell_books)
```
**Output:**
```
<QuerySet [<Book: 1984, George Orwell, 1949 >, <Book: Animal Farm, George Orwell, 1945 >]>
```

### Get Book by ID
```python
book = Book.objects.get(id=1)
print(f"ID: {book.id}, Title: {book.title}")
```
**Output:**
```
ID: 1, Title: 1984
```

## UPDATE Operations

### Update Single Field
```python
book = Book.objects.get(title="1984")
book.publication_year = 1950
book.save()
print(book)
```
**Output:**
```
1984, George Orwell, 1950 
```

### Update Using update() Method
```python
Book.objects.filter(title="1984").update(publication_year=1949)
updated_book = Book.objects.get(title="1984")
print(updated_book)
```
**Output:**
```
1984, George Orwell, 1949 
```

### Update Multiple Fields
```python
book = Book.objects.get(title="Animal Farm")
book.author = "George Orwell (Updated)"
book.publication_year = 1946
book.save()
print(book)
```
**Output:**
```
Animal Farm, George Orwell (Updated), 1946 
```

## DELETE Operations

### Delete Specific Book
```python
book = Book.objects.get(title="Animal Farm")
result = book.delete()
print(result)
```
**Output:**
```
(1, {'bookshelf.Book': 1})
```

### Delete Using Filter
```python
# Create a book to delete
Book.objects.create(title="Brave New World", author="Aldous Huxley", publication_year=1932)

# Delete it
deleted_count = Book.objects.filter(title="Brave New World").delete()
print(deleted_count)
```
**Output:**
```
(1, {'bookshelf.Book': 1})
```

### Verify Deletion
```python
try:
    book = Book.objects.get(title="Brave New World")
    print("Book found")
except Book.DoesNotExist:
    print("Book not found - successfully deleted")
```
**Output:**
```
Book not found - successfully deleted
```

## Final Verification
```python
# Check remaining books
remaining_books = Book.objects.all()
print(f"Total books: {remaining_books.count()}")
for book in remaining_books:
    print(f"- {book}")
```
**Output:**
```
Total books: 1
- 1984, George Orwell, 1949 
```