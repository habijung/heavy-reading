from django.db import models

# Create your models here.
class UserAccount(models.Model):
    email = models.CharField(max_length = 200)
    password = models.CharField(max_length = 200)
    pub_date = models.DateTimeField('date published')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'accounts'