from ast import Mod
from dataclasses import field
from admins.models import Admin,JobFair,JobFairRegister
from django import forms
from django.forms import ModelForm
from home.models import JobCategory,Jobs

class AdminForm(ModelForm):

    password = forms.CharField(widget=forms.PasswordInput(attrs={ 'class': 'form-control text-white'}))
    admin_name = forms.CharField(widget=forms.TextInput(attrs={ 'class' : 'form-control text-white'}))

    class Meta:
        model = Admin
        fields = ['admin_name','password']
        
class CategoryForm(ModelForm):
    class Meta:
        model = JobCategory
        fields = ['category_name']
        
class DateInput(forms.DateInput):
    input_type = 'date'
    
class JobFairAddForm(ModelForm):
    class Meta:
        model = JobFair
        fields = ('job_fair_name','conducted_date')
        widgets = {
            'conducted_date': DateInput(),
          
        }