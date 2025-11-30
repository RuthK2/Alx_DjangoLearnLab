# Advanced API Project - Django REST Framework

## Overview
This project implements a RESTful API using Django REST Framework with custom views for CRUD operations on Book and Author models, including advanced query capabilities.

## API Endpoints

### Books
- `GET /api/books/` - List all books with filtering, search, and ordering
- `GET /api/books/<id>/` - Retrieve single book (public access)
- `POST /api/books/create/` - Create new book (authentication required)
- `PUT /api/books/update/` - Update existing book (authentication required)
- `DELETE /api/books/delete/` - Delete book (authentication required)

## Advanced Query Features

### Filtering
Filter books by specific fields:
- `GET /api/books/?title=Harry Potter` - Filter by exact title
- `GET /api/books/?author__name=J.K. Rowling` - Filter by author name
- `GET /api/books/?publication_year=1997` - Filter by publication year

### Search
Search across title and author fields:
- `GET /api/books/?search=Harry` - Search for "Harry" in title or author name

### Ordering
Order results by any field:
- `GET /api/books/?ordering=title` - Order by title (ascending)
- `GET /api/books/?ordering=-publication_year` - Order by year (descending)
- `GET /api/books/?ordering=title,publication_year` - Multiple field ordering

### Combined Queries
Combine filtering, search, and ordering:
- `GET /api/books/?search=Potter&ordering=-publication_year&author__name=J.K. Rowling`

## View Configurations

### BookList (ListAPIView)
- **Purpose**: Retrieve all books with advanced query capabilities
- **Permissions**: IsAuthenticatedOrReadOnly (public read access)
- **Features**: 
  - Filtering by title, author name, publication year
  - Search across title and author name
  - Ordering by title and publication year
  - Default ordering by title

### Authentication
Get token: `POST /api/auth/token/` with username/password
Use token: `Authorization: Token YOUR_TOKEN_HERE`

## Models
- **Author**: Basic author information with name field
- **Book**: Book details with title, publication_year (validated), and author relationship

## Validation
- Publication year must be between 1000 and current year + 10
- Custom serializer validation prevents future publication dates