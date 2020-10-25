from django.shortcuts import render
from mainpage.views import Report, Rating, Memo

# Create your views here.

def users(request):
    reports = Report.objects.filter(user=request.user)
    ratings = Rating.objects.filter(user=request.user)
    memos = Memo.objects.filter(user=request.user)
    return render(request, 'userpage.html', {'reports':reports, 'ratings':ratings,'memos':memos})