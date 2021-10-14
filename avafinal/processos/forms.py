from django import forms
from django.forms import fields
from .models import Process

class ProcessForm(forms.ModelForm):
    class Meta:
        model = Process
        fields = ('title', 'description')