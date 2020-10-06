from django.shortcuts import render, get_object_or_404
from .models import Book
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
# Create your views here.
def main(request):
    books = Book.objects
    return render(request, 'main.html', {'books': books})

def detail(request, book_id):
    book_info = get_object_or_404(Book, pk=book_id)
    return render(request, 'detail.html', {'book':book_info})