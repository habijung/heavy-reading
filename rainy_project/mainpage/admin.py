from django.contrib import admin
from .models import Book, Report, Rating, Memo

# Register your models here.
admin.site.register(Book)
admin.site.register(Report)
admin.site.register(Rating)
admin.site.register(Memo)