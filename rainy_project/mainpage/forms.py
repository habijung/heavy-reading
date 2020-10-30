from django import forms
from django.db import models

from .models import Memo

class MemoForm(forms.ModelForm):

    class Meta:
        model = Memo
        fields = ['page', 'phrase']