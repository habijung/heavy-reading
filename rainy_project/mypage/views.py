from django.shortcuts import render
from mainpage.views import Report, Rating, Memo

# Create your views here.

def users(request):
    return render(request, 'userpage.html')

def my_rating(request):
    ratings = Rating.objects.filter(user=request.user)
    return render(request, 'my_rating.html', {'ratings':ratings})

def my_report(request):
    reports = Report.objects.filter(user=request.user)
    return render(request, 'my_report.html', {'reports':reports})

def my_memo(request):
    memos = Memo.objects.filter(user=request.user)
    return render(request, 'my_memo.html', {'memos':memos})