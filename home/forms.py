
from tkinter.tix import Form
from django.forms import ModelForm
from django import forms
from home.models import Jobs,JobCategory,AppliedJobs,SpamCompanies
from home.models import Companies
from admins.models import JobFair,JobFairRegister
import datetime

class JObAddForm(ModelForm):
      
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(JObAddForm, self).__init__(*args, **kwargs)
        self.fields['company'].queryset = Companies.objects.filter(
            recruiter=self.request.user)
        self.fields['job_description'].widget.attrs = {'rows': 2}
    
    category_ = forms.CharField(max_length=100)    
    company = forms.ModelChoiceField(queryset=Companies.objects.all())
    
    class Meta:
        model = Jobs
        fields = ['title','category_','salary','location','company','job_description','vacancies','experience','job_type']
# Logics are applied, its inheriting from teh parent class
# just overirding the parent Meta class 
# category is now taking from the category foreign key
# in the parent form its related to the recruiter desire, he can eter the 
# category manually 
class JobEditForm(JObAddForm):
    
    JObAddForm.category_ = None
    class Meta(JObAddForm.Meta):
        model = Jobs
        fields = ['title','category','salary','location','company','job_description','vacancies','experience','job_type']  
           
class ApplyJobForm(ModelForm):
    
    class Meta:
        model = AppliedJobs
        fields = ('resume',)
        
class SpamCompaniesForm(ModelForm):
    
    class Meta:
        model = SpamCompanies
        fields = ('reason',)
        
        
class JobFairRegisterForm(ModelForm):
    
    today = datetime.datetime.today()
    
    def __init__(self,*args,**kwargs):
        self.request = kwargs.pop("request")
        super(JobFairRegisterForm,self).__init__(*args,**kwargs)
        self.fields['company'].queryset = Companies.objects.filter(recruiter=self.request.user)
        self.fields['jobfair'].queryset  = JobFair.objects.filter(conducted_date__gte=self.today)
        
    class Meta:
        model = JobFairRegister
        fields = ('company','jobfair')
        
    company=forms.ModelChoiceField(queryset=None)
    jobfair=forms.ModelChoiceField(queryset=None)





class JobFairSearch(forms.Form):
    close_date = forms.DateField(input_formats=['%m/%d/%Y'],widget=forms.DateInput())