from django.contrib import admin
from .models import Book, Report, Rating

# Register your models here.
admin.site.register(Book)
admin.site.register(Report)
admin.site.register(Rating)