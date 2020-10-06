from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    cover = models.ImageField(upload_to='images/', blank=True)
    pub_date = models.DateTimeField('date published')
    value = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    summary = models.TextField()
    author = models.CharField(max_length=50)
    paragraph = models.TextField()
    count = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.title

class Report(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    text = models.TextField()
    pub_date = models.DateTimeField('date published')