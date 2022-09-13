from accounts.models import Account,Companies,Intrests, UserProfile
from home.models import JobCategory
from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ('first_name','last_name','email','phone','role','password1','password2')
        
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['password1', 'password2']:
            self.fields[fieldname].help_text = None
            
class CompaniesForm(ModelForm):
    class Meta:
        model = Companies
        fields = ('company_name','email','contact_number','image','country','places')

# Intrests creation models 

INTREST_CHOICES = tuple(((i.category_name,i.category_name) for i in JobCategory.objects.all()))

class IntrestForm(forms.Form):
    inrests = forms.MultipleChoiceField(choices = INTREST_CHOICES)
    
    
class IntrestEditForm(forms.Form):
    inrests = forms.MultipleChoiceField(choices = INTREST_CHOICES)
        
class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profile_pic','first_name','last_name','username','email','phone','country','state','city')
