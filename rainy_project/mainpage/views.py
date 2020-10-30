from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import Book, Report, Rating, Memo, Survey
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils import timezone
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt
from .forms import MemoForm
from django.contrib import messages
from django.http import JsonResponse

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
    opened_report = Report.objects.filter(book=book_info, approved_open=True)
    page = int(request.GET.get('p', 1))
    paginator = Paginator(opened_report, 10)
    reports = paginator.get_page(page)
    if request.user.is_authenticated:
        try:
            my_grade = Rating.objects.get(book=book_info, user=request.user)
            return render(request, 'detail.html', {'book':book_info, 'reports':reports, 'my_grade':my_grade.grade})
        except Rating.DoesNotExist:
            my_grade = 0
            return render(request, 'detail.html', {'book':book_info, 'reports':reports, 'my_grade':my_grade})
    return render(request, 'detail.html', {'book':book_info, 'reports':reports})

def detail_opened_report(request, report_id):
    report = get_object_or_404(Report, pk=report_id)
    return render(request, "detail_opened_report.html", {"report":report})

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

    try:
        my_grade = Rating.objects.get(book=book, user=request.user)
        return render(request, 'create_report_page.html', {'book':book, 'report':report, 'my_grade':my_grade.grade})
    except Rating.DoesNotExist:
        my_grade = 0
        return render(request, 'create_report_page.html', {'book':book, 'report':report, 'my_grade':my_grade})

def create_memo_page(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    form = MemoForm()

    try:
        my_grade = Rating.objects.get(book=book, user=request.user)
        return render(request, 'create_memo_page.html', {'book':book, 'form':form, 'my_grade':my_grade.grade})
    except Rating.DoesNotExist:
        my_grade = 0
        return render(request, 'create_memo_page.html', {'book':book, 'form':form, 'my_grade':my_grade})

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
        memo = Memo()

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

    return JsonResponse({'grade':round(Decimal(book.grade), 1), 'my_grade':rating.grade, 'count':book.count})

def survey(request):
    return render(request, "survey_form.html")

def submit_survey(request):
    title = request.POST['title']
    author = request.POST['author']
    try:
        survey = Survey.objects.get(title=title, author=author)
        user = survey.user.all()
        if request.user in user:
            messages.error(request, "이미 신청하신 책입니다.")
        else:
            survey.count = survey.count + 1
            survey.user.add(request.user)
            survey.save()
            messages.success(request, "신청되었습니다.")
    except Survey.DoesNotExist:
        survey = Survey()
        survey.title = title
        survey.author = author
        survey.count = 1
        survey.save()
        survey.user.add(request.user)
        messages.success(request, "신청되었습니다.")

    return redirect('/survey_form')