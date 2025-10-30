# Create Operation - Django Shell

## Command
```python
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
print(book)
```

## Expected Output
```
1984, George Orwell, 1949 
```

## Alternative Method
```python
from bookshelf.models import Book
book = Book(title="1984", author="George Orwell", publication_year=1949)
book.save()
print(book)
```

## Verification
```python
# Check if the book was created successfully
Book.objects.filter(title="1984").exists()  # Returns: True
```