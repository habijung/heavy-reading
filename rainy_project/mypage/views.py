from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from mainpage.views import Report, Rating, Memo

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
    return render(request, 'my_memo.html', {'memos':memos})