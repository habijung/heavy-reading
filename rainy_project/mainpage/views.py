from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Report, Rating, Memo
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils import timezone
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt
from .forms import MemoForm

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

@csrf_exempt
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
    try:
        report = Report.objects.get(book=book, user=request.user)
    except Report.DoesNotExist:
        report = -1
    return render(request, 'create_report_page.html', {'book':book, 'report':report})

def create_memo_page(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    form = MemoForm()
    return render(request, 'create_memo_page.html', {'book':book, 'form':form})

def create_report(request, book_id):
    if request.method == "POST":
        book = get_object_or_404(Book, pk=book_id)
        try:
            report = Report.objects.get(book=book, user=request.user)
        except Report.DoesNotExist:
            report = Report()

        report.title = request.POST['title']
        report.text = request.POST['text']
        report.pub_date = timezone.datetime.now()
        report.book = book
        report.user = request.user
        if request.POST.get('is_open') == "True":
            report.approved_open = True
        else:
            report.approved_open = False

        report.save()

        return redirect('/create_report_page/' + str(book_id))

def report_del(request, report_id):
    if request.method == "POST":
        report_delete = get_object_or_404(Report, pk=report_id)
        book_id = report_delete.book.id
        report_delete.delete()
        return redirect('/detail/' + str(book_id))

'''
def create_memo(request, book_id):
    if request.method == 'POST':
        book = get_object_or_404(Book, pk=book_id)
        form = MemoForm(request.POST, request.FILES)
        if form.is_valid():
            memo = Memo(**form.cleaned_data)
            memo.book = book
            memo.pub_date = timezone.datetime.now()
            memo.user = request.user
            memo.save()

            return redirect('/detail/' + str(book_id))
'''

def create_memo(request, book_id):
    if request.method == 'POST':
        book = get_object_or_404(Book, pk=book_id)
        memo = Memo();

        memo.page = request.POST['page']
        memo.phrase = request.POST['phrase']
        memo.book = book
        memo.pub_date = timezone.datetime.now()
        memo.user = request.user
        memo.save()

        return redirect('/detail/' + str(book_id))

@csrf_exempt
def rating(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    try:
        rating = Rating.objects.get(book=book, user=request.user)
        temp = rating.grade
        rating.grade = request.POST['vote']
        rating.pub_date = timezone.datetime.now()
        rating.book = book
        rating.user = request.user
        rating.save()
        book.grade = book.grade - Decimal(temp / book.count)
        book.grade = book.grade + Decimal(int(rating.grade) / book.count)
    except Rating.DoesNotExist:
        rating = Rating()
        rating.grade = request.POST['vote']
        rating.pub_date = timezone.datetime.now()
        rating.book = book
        rating.user = request.user
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