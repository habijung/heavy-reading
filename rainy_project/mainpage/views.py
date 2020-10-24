from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Report, Rating, Memo
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils import timezone
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt

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

@csrf_exempt
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

def create_report_page(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'create_report_page.html', {'book':book})

def create_memo_page(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'create_memo_page.html', {'book':book})

def create_report(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    report = Report()

    report.title = request.POST['title']
    report.text = request.POST['text']
    report.pub_date = timezone.datetime.now()
    report.book = book

    report.save()

    return redirect('/detail/' + str(book_id))

def create_memo(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    memo = Memo()

    memo.book = book
    memo.page = request.POST['page']
    memo.phrase = request.POST['text']
    memo.pub_date = timezone.datetime.now()
    memo.save()

    return redirect('/detail/' + str(book_id))

@csrf_exempt
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