from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    affiliation = models.IntegerField(default=5)

    class Meta:
        verbose_name = "User Profile Name"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return self.user.username