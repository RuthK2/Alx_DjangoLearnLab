from django.db import models

# Author model to store author information
class Author(models.Model):
    name = models.CharField(max_length=100)  # Author's name
    
    def __str__(self):
        return self.name

# Book model with foreign key relationship to Author
class Book(models.Model):
    title = models.CharField(max_length=200)  # Book title
    publication_year = models.IntegerField()  # Year published
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')  # One-to-many relationship
    
    def __str__(self):
        return self.title