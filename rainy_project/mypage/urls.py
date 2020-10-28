from django.urls import path

from . import views

urlpatterns = [
    path('', views.users, name='users'),
    path('my_rating/', views.my_rating, name='my_rating'),
    path('my_report/', views.my_report, name='my_report'),
    path('my_memo/', views.my_memo, name='my_memo'),
    path('my_report/<int:report_id>', views.detail_report, name='detail_report'),
    #path('my_report_delete/', views.my_report_delete, name='my_report_delete'),
]