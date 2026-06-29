from django.forms import ModelForm
from .models import Employee

from django import forms

class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        widgets = {
            'joining_date': forms.DateInput(attrs={'type': 'date'}),
        }