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



@login_required
@permission_required('bookshelf.can_view_book', raise_exception=True)
def book_detail(request, pk):
    book = Book.objects.get(pk=pk)
    return render(request, 'book_detail.html', {'book': book})

@login_required
@permission_required('bookshelf.can_create_book', raise_exception=True)
def book_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        year = request.POST.get('publication_year')
        Book.objects.create(title=title, author=author, publication_year=year)
        return redirect('bookshelf:list')  # redirect after create
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
