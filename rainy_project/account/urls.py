from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.SignUpView.as_view()),
    path('up/', views.SignUpView.as_view()),
    path('in/', views.SignInView.as_view()),
]