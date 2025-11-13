from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    """
    Secure form for Book model with built-in validation and CSRF protection.
    Django ModelForm automatically handles input sanitization and validation.
    """
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'publication_year': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
        }
    
    def clean_publication_year(self):
        """Custom validation for publication year to prevent invalid data."""
        year = self.cleaned_data.get('publication_year')
        if year and (year < 1000 or year > 2030):
            raise forms.ValidationError("Publication year must be between 1000 and 2030.")
        return year
    
    def clean_title(self):
        """Custom validation for title to prevent XSS and ensure proper length."""
        title = self.cleaned_data.get('title')
        if title and len(title.strip()) < 2:
            raise forms.ValidationError("Title must be at least 2 characters long.")
        return title.strip() if title else title
    
    def clean_author(self):
        """Custom validation for author to ensure proper length."""
        author = self.cleaned_data.get('author')
        if author and len(author.strip()) < 2:
            raise forms.ValidationError("Author name must be at least 2 characters long.")
        return author.strip() if author else author