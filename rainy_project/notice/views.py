from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Notice

def notice(request):
    notice_all = Notice.objects.all().order_by('-pub_date')
    page = int(request.GET.get('p', 1))
    paginator = Paginator(notice_all, 10)
    notices = paginator.get_page(page)
    
    return render(request, "notice.html", {"notices":notices})

def detail_notice(request, notice_id):
    notice = get_object_or_404(Notice, pk=notice_id)
    return render(request, "detail_notice.html", {"notice":notice})