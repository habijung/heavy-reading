from django.shortcuts import render, get_object_or_404
from .models import Book

# Create your views here.
def main(request):
    books = Book.objects
    return render(request, 'main.html', {'books': books})

def detail(request, book_id):
    book_info = get_object_or_404(Book, pk=book_id)
    return render(request, 'detail.html', {'book':book_info})

def search(request):
    books = Book.objects.all()

    q = request.POST.get('q', "")

    if q:
        books = books.filter(title__icontains=q)
        return render(request, 'search.html', {'books': books, 'q': q})

    else:
        return render(request, 'search.html')