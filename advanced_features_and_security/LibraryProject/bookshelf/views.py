# Security: Import secure Django functions to prevent SQL injection and handle errors safely
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required, permission_required
from .models import Book

def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})

class Booklist(ListView):
    model = Book
    template_name = 'book_list.html'
    context_object_name = 'books'



# Security: Require authentication and permissions, use get_object_or_404 to prevent SQL injection
@login_required
@permission_required('bookshelf.can_view_book', raise_exception=True)
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)  # Safe query - prevents DoesNotExist errors
    return render(request, 'book_detail.html', {'book': book})

# Security: Protected by authentication, permissions, and CSRF token in template
@login_required
@permission_required('bookshelf.can_create_book', raise_exception=True)
def book_create(request):
    if request.method == 'POST':
        # Security: Using request.POST.get() safely handles user input
        title = request.POST.get('title')
        author = request.POST.get('author')
        year = request.POST.get('publication_year')
        # Security: ORM create() method prevents SQL injection
        Book.objects.create(title=title, author=author, publication_year=year)
        return redirect('bookshelf:list')  # Security: Redirect prevents duplicate submissions
    return render(request, 'book_form.html')

@login_required
@permission_required('bookshelf.can_edit_book', raise_exception=True)
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.publication_year = request.POST.get('publication_year')
        book.save()
        return redirect('bookshelf:list')
    return render(request, 'book_form.html', {'book': book})

@login_required
@permission_required('bookshelf.can_delete_book', raise_exception=True)
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('bookshelf:list')
    return render(request, 'book_confirm_delete.html', {'book': book})
