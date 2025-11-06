from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Book, Library
def list_books(request):
    books = Book.objects.all()
    return render(request, 'list_books.html', {'books': books})
# Create your views here.
class Booklist(ListView):
    model = Book
    template_name = 'list_books.html'
    context_object_name = 'books'

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'library_detail.html'
    context_object_name = 'library'