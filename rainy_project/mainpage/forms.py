from django import forms
from django.db import models

from .models import Memo

class MemoForm(forms.ModelForm):
    '''
    page = forms.IntegerField(widget=forms.NumberInput),
    phrase = forms.TextInput(widget=forms.TextInput)
    '''

    class Meta:
        model = Memo
        fields = ['page', 'phrase']