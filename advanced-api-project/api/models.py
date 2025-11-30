from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime

def get_max_year():
    return datetime.now().year + 10

# Author model to store author information
class Author(models.Model):
    name = models.CharField(max_length=100)  # Author's name
    
    def __str__(self):
        return self.name

# Book model with foreign key relationship to Author
class Book(models.Model):
    title = models.CharField(max_length=200)  # Book title
    publication_year = models.IntegerField(
        validators=[
            MinValueValidator(1000),
            MaxValueValidator(get_max_year())
        ]
    )  # Year published with validation
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books') 
     # One-to-many relationship
    
    def __str__(self):
        return self.title
    