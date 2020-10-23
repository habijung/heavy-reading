from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Profile

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = Profile
        fields = UserCreationForm.Meta.fields + ('affiliation',)

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = Profile
        fields = UserChangeForm.Meta.fields