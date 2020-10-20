from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import Thumbnail

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    cover = models.ImageField(upload_to='images/')
    cover_thumbnail = ImageSpecField(
        source = 'cover',
        processors = [Thumbnail(280, 370)],
        format = 'JPEG',
        options = {'quality' : 60}
    )
    pub_date = models.DateTimeField('date published')
    grade = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    body = models.TextField()
    author = models.CharField(max_length=50)
    count = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.title

class Report(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    title = models.CharField(default='', max_length=200)
    text = models.TextField()
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.title

class Rating(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    grade = models.SmallIntegerField(default=0)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.book.title