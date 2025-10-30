# Update Operation - Django Shell

## Update Single Book
```python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"  # Update title
book.save()
print(book)
```

## Expected Output
```
Nineteen Eighty-Four, George Orwell, 1949 
```

## Update Using update() Method
```python
Book.objects.filter(title="1984").update(title="Nineteen Eighty-Four")
# Retrieve to verify
updated_book = Book.objects.get(title="Nineteen Eighty-Four")
print(updated_book)
```

## Expected Output
```
Nineteen Eighty-Four, George Orwell, 1949 
```

## Update Multiple Fields
```python
book = Book.objects.get(title="1984")
book.author = "George Orwell (Updated)"
book.publication_year = 1948
book.save()
print(book)
```