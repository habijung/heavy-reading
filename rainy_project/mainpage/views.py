from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Report, Rating
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils import timezone
from decimal import Decimal

def main(request):
    sort = request.GET.get('sort','')

    if sort == 'reverse' :
        books = Book.objects.all().order_by('pub_date')
    elif sort == 'grade' :
        books = Book.objects.order_by('-grade', '-count', '-pub_date')
    else :
        books = Book.objects.all().order_by('-pub_date')
    paginator = Paginator(books, 12)
    page = request.POST.get('page')

    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = {}

    return render(request, 'main.html', {'books': books})

def main_ajax(request):
    sort = request.GET.get('sort','')

    if sort == 'reverse' :
        books = Book.objects.all().order_by('pub_date')
    elif sort == 'grade' :
        books = Book.objects.order_by('-grade', '-count', '-pub_date')
    else :
        books = Book.objects.all().order_by('-pub_date')

    paginator = Paginator(books, 12)
    page = request.POST.get('page')

    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = {}

    return render(request, 'main_ajax.html', {'books': books})


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

def create_report(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'create_report.html', {'book':book})

def create(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    report = Report()

    report.title = request.POST['title']
    report.text = request.POST['text']
    report.pub_date = timezone.datetime.now()
    report.book = book
    report.save()

    return redirect('/detail/' + str(book_id))

def rating(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    rating = Rating()
    rating.grade = request.POST['vote']
    rating.pub_date = timezone.datetime.now()
    rating.book = book
    rating.save()

    if book.count == 0 :
        book.grade = rating.grade
        book.count = 1
    else :
        temp = book.count / (book.count + 1)
        book.count = book.count + 1
        book.grade = book.grade * Decimal(temp)
        temp = int(rating.grade) / book.count
        book.grade = book.grade + Decimal(temp)
        
    book.save()

    return redirect('/detail/' + str(book_id))