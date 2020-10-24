from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Profile

# Register your models here.
class ProfileInline(admin.StackedInline):  
    model = Profile
    can_delete = False
    verbose_name = "User Profile Name"
    verbose_name_plural = 'Profile'

class UserAdmin(UserAdmin):  
    inlines = (ProfileInline, )

class ProfileAdmin(admin.ModelAdmin):
    fields = ['password']

admin.site.unregister(User)  
admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)