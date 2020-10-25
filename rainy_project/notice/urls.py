from django.urls import path

from . import views

urlpatterns = [
    path('', views.notice, name='notice'),
    path('detail/<int:notice_id>', views.detail_notice, name='detail_notice'),
]