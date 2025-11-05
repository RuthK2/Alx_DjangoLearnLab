from relationship_app.models import Author, Book, Library, Librarian

# Create sample data
author, created = Author.objects.get_or_create(name="George Orwell")
book1, created = Book.objects.get_or_create(title="1984", author=author)
book2, created = Book.objects.get_or_create(title="Animal Farm", author=author)
library, created = Library.objects.get_or_create(name="Central Library")
library.books.add(book1, book2)
librarian, created = Librarian.objects.get_or_create(name="Alice Johnson", library=library)

# Query all books by a specific author
author_name = "George Orwell"
author = Author.objects.get(name=author_name)
books_by_author = Book.objects.filter(author=author)
print(f"Books by {author_name}:")
for book in books_by_author:
    print(f"- {book.title}")

# List all books in a library
library_name = "Central Library"
library = Library.objects.get(name=library_name)
books_in_library = library.books.all()
print(f"\nBooks in {library_name}:")
for book in books_in_library:
    print(f"- {book.title}")

# Retrieve the librarian for a library
library = Library.objects.get(name="Central Library")
librarian = library.librarian
print(f"\nLibrarian for {library.name}: {librarian.name}")