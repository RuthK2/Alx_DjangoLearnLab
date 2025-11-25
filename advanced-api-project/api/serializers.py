from rest_framework import serializers
from django.utils import timezone
from .models import Book, Author

# BookSerializer: Serializes all fields of the Book model
# Includes custom validation for publication_year
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'  # Serializes all fields: title, publication_year, author

    def validate_publication_year(self, value):
        """
        Custom validation to ensure publication year is not in the future.
        Prevents books from having publication dates beyond the current year.
        """
        current_year = timezone.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future (current year is {current_year})."
            )
        return value

# AuthorSerializer: Serializes Author model with nested books
# Demonstrates one-to-many relationship handling through nested serialization
class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)  # Nested serializer for related books
    
    # Relationship handling:
    # - 'books' field uses the related_name from the ForeignKey in Book model
    # - 'many=True' because one author can have multiple books (one-to-many)
    # - 'read_only=True' prevents creation of books through author serializer
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']  # Include name field and nested books