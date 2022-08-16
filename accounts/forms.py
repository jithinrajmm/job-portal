from accounts.models import Account,Companies
from django.forms import ModelForm
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

