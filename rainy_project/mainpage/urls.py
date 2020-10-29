from django.urls import path

from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('detail/<int:book_id>', views.detail, name='detail'),
    path('search/', views.search, name='search'),
    path('main/ajax', views.main_ajax, name='main_ajax'),
    path('create_report_page/<int:book_id>', views.create_report_page, name='create_report_page'),
    path('create_memo_page/<int:book_id>', views.create_memo_page, name='create_memo_page'),
    path('create_report/<int:book_id>', views.create_report, name='create_report'),
    path('create_memo/<int:book_id>', views.create_memo, name='create_memo'),
    path('rating/<int:book_id>', views.rating, name='rating'),
    path('detail_opened_report/<int:report_id>', views.detail_opened_report, name='detail_opened_report'),
    path('survey_form/', views.survey, name='survey'),
    path('submit_survey/', views.submit_survey, name='submit_survey'),
]