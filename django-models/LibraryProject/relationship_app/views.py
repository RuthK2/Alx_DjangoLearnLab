from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Book, Library
def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})
# Create your views here.
class Booklist(ListView):
    model = Book
    template_name = 'book_list.html'
    context_object_name = 'books'

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'library_detail.html'
    context_object_name = 'library'