from django.contrib import admin
from .models import Book, Report, Rating, Memo, Survey

# Register your models here.
admin.site.register(Book)
admin.site.register(Report)
admin.site.register(Rating)
admin.site.register(Memo)
admin.site.register(Survey)