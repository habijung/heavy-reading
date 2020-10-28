from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from mainpage.views import Report, Rating, Memo
import math

# Create your views here.

def users(request):
    return render(request, 'userpage.html')

def my_rating(request):
    ratings = Rating.objects.filter(user=request.user)
    return render(request, 'my_rating.html', {'ratings':ratings})

def my_report(request):
    reports_all = Report.objects.filter(user=request.user)
    page = int(request.GET.get('p', 1))
    paginator = Paginator(reports_all, 10)
    reports = paginator.get_page(page)
    return render(request, 'my_report.html', {'reports':reports})

def detail_report(request, report_id):
    report = get_object_or_404(Report, pk=report_id)
    return render(request, "detail_report.html", {"report":report})

def my_memo(request):
    memos = Memo.objects.filter(user=request.user)
    memos = memos.order_by('?')
    rows = math.ceil(memos.count() / 4)
    rows = range(0, rows)
    cols = range(0, 4)

    memos_matrix = []
    count = 0
    chk = 0
    for col in cols:
        memos_matrix.append([])
        for row in rows:
            memos_matrix[col].append(memos[count])
            count = count + 1
            if count == memos.count() :
                chk = 1
                break
        if chk == 1:
            break

    
    return render(request, 'my_memo.html', {'memos':memos_matrix, 'rows':rows, 'cols':cols})

def my_report_delete(request, report_id):
    if request.method == "POST":
        report_delete = get_object_or_404(Report, pk=report_id)
        book_id = report_delete.book.id
        report_delete.delete()
        return redirect('/users/my_report/')