# Advanced API Project - Django REST Framework

## Overview
This project implements a RESTful API using Django REST Framework with custom views for CRUD operations on Book and Author models.

## API Endpoints

### Books
- `GET /api/books/` - List all books (public access)
- `GET /api/books/<id>/` - Retrieve single book (public access)
- `POST /api/books/create/` - Create new book (authentication required)
- `PUT /api/books/<id>/update/` - Update existing book (authentication required)
- `DELETE /api/books/<id>/delete/` - Delete book (authentication required)

## View Configurations

### BookList (ListAPIView)
- **Purpose**: Retrieve all books
- **Permissions**: IsAuthenticatedOrReadOnly (public read access)
- **Custom Features**: None

### BookDetail (RetrieveAPIView)
- **Purpose**: Retrieve single book by ID
- **Permissions**: IsAuthenticatedOrReadOnly (public read access)
- **Custom Features**: None

### BookCreate (CreateAPIView)
- **Purpose**: Create new book instances
- **Permissions**: IsAuthenticated (requires login)
- **Custom Features**: Automatic data validation via serializer

### BookUpdate (UpdateAPIView)
- **Purpose**: Update existing book instances
- **Permissions**: IsAuthenticated (requires login)
- **Custom Features**: Partial updates supported

### BookDelete (DestroyAPIView)
- **Purpose**: Delete book instances
- **Permissions**: IsAuthenticated (requires login)
- **Custom Features**: Soft delete not implemented

## Models
- **Author**: Basic author information with name field
- **Book**: Book details with title, publication_year (validated), and author relationship

## Validation
- Publication year must be between 1000 and current year + 10
- Custom serializer validation prevents future publication dates