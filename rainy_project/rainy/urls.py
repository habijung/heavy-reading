"""rainy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import mainpage.views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', mainpage.views.main, name='main'),
    path('detail/<int:book_id>', mainpage.views.detail, name='detail'),
    path('search/', mainpage.views.search, name='search'),
    path('main/ajax', mainpage.views.main_ajax, name='main_ajax'),
    path('create_report/<int:book_id>', mainpage.views.create_report, name='create_report'),
    path('create/<int:book_id>', mainpage.views.create, name='create'),
    path('rating/<int:book_id>', mainpage.views.rating, name='rating'),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
