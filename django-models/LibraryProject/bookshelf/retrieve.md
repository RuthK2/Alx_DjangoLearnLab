# Retrieve Operation - Django Shell

## Get All Books
```python
from bookshelf.models import Book
books = Book.objects.all()
print(books)
```

## Expected Output
```
<QuerySet [<Book: 1984, George Orwell, 1949 >]>
```

## Get Specific Book by Title
```python
book = Book.objects.get(title="1984")
print(book)
```

## Expected Output
```
1984, George Orwell, 1949 
```

## Filter Books by Author
```python
orwell_books = Book.objects.filter(author="George Orwell")
print(orwell_books)
```

## Get Book by ID
```python
book = Book.objects.get(id=1)  # Assuming it's the first book created
print(f"ID: {book.id}, Title: {book.title}")
```