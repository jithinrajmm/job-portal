from email import message
from django.shortcuts import render

# Create your views here.

from django.shortcuts import redirect, render

# for user login
from django.contrib.auth.forms import AuthenticationForm

from accounts.forms import CustomUserCreationForm,CompaniesForm

# class based views
from django.views import View
from django.contrib.auth import authenticate,login,logout

# Databases 
from accounts.models import Account

# flash messages 
from django.contrib import messages 

# for redirecting the user to the login
import requests
from django.urls import resolve
from urllib.parse import urlparse





# Create your views here.
def user_login(request):
    forms = AuthenticationForm()
    if request.method == 'POST':
        forms = AuthenticationForm(request,data = request.POST)
        
        if forms.is_valid():
            username = forms.cleaned_data.get('username')
            password = forms.cleaned_data.get('password')
            user = authenticate(username=username,password=password)

            if user is not None:
                if user.role == 'recruiter' and user.is_recruiter == False:
                    messages.error(request, "Please contact to Admin For verification")
                    return redirect('home')
                else:
                    login(request,user)
                    messages.success(request, "login Success")
                    # where the request is came , redirect the user to that 
                    # page if its is a success login
                    url = request.META.get('HTTP_REFERER')
                    url_parser = urlparse(url)
                    # http://127.0.0.1:8000/accounts/user_login/?next=/apply_job/3/
                    # from this we are taking the last path
                    if url_parser.query:
                        path = url_parser.query.split('=')
                        return redirect(path[1])
                    else:
                        return redirect('home')



                
        else:
            print(forms.errors)
    context = {
      'form': forms,  
    }
    return render(request,'user/login.html',context)
    
    
class UserCreation(View):
    ''' user creation view used the class based view '''
    
    template_name = 'user/register.html'
    form_class = CustomUserCreationForm
    
    def get(self, request,*args,**kwargs):
        context = {
            'form': self.form_class
        }
        if request.session.get('recruiter'):
            id = request.session.get('recruiter')
            user = Account.objects.get(id=id)
            user.delete()
            try:
                del request.session['recruiter']
            except:
                pass
            
        return render(request,self.template_name,context)
        
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = new_user.email[0: new_user.email.index('@')]
            new_user.is_active = True
            new_user.save()
            if new_user.role == 'recruiter':
                request.session['recruiter'] = new_user.id
                return redirect('company_register')
            else:
                return redirect('home')
                  
        return render(request, self.template_name, {'form': form})
        
def company_register(request):
    form = CompaniesForm()
    context = {
        'form':  form,
    }
    
    if request.method == 'POST':
        form = CompaniesForm(request.POST,request.FILES)
        if form.is_valid():
            company = form.save(commit=False)
            if request.session.get('recruiter'):
                id = request.session.get('recruiter')
                company.recruiter = Account.objects.get(id=id)
                company.save()
                try:
                    del request.session['recruiter']
                except:
                    pass    
            return redirect('home')
     
    return render(request,'recruiter/add_company.html',context)
   
def logout_view(request):
    ''' logout view of the user , '''
    
    logout(request)
    return redirect('home')
    

