
from django.shortcuts import render
# Create your views here.
from django.shortcuts import redirect, render
# form user login FORM'S 
from django.contrib.auth.forms import AuthenticationForm
from accounts.forms import CustomUserCreationForm,CompaniesForm,IntrestForm,UserProfileForm,IntrestEditForm
# class based views
from django.views import View
# authentication
from django.contrib.auth import authenticate,login,logout
# Databases 
from accounts.models import Account,Intrests,UserProfile,Counts
# flash messages 
from django.contrib import messages 
# for redirecting the user to the login
import requests
from urllib.parse import urlparse
# fo F() Expression
from django.db.models import F,Sum,Count,Avg
# import get_object_or_404()
from django.shortcuts import get_object_or_404

from home.models import JobCategory


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
            elif new_user.role == 'applicant':
                request.session['user'] = new_user.id
                return redirect('user_intrests')
            else:
                return redirect('home')
                  
        return render(request, self.template_name, {'form': form})
        
def user_intrests(request):
    
    form = IntrestForm()
    
    if request.method == 'POST':
        form = IntrestForm(request.POST)
        if form.is_valid():
            intrests = form.cleaned_data.get("inrests")
            id = request.session.get('user')
            user = Account.objects.get(id=id)
            for intrest in intrests:
                intrest_object = Intrests.objects.create(user=user,intrest=intrest)
                intrest_object.save()
            intrest = Intrests.objects.filter(user=id)
            messages.success(request,'Registraiton success')
            return redirect('home')
                
    
    context = {
        'form':form,
    }
    return render(request,'user/intrest_form.html',context) 
    
def company_register(request):
    form = CompaniesForm()
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
            
    context = {
        'form':  form,
    }
    return render(request,'recruiter/add_company.html',context)
    
def user_profile(request):
    user_profile = UserProfile.objects.get(user=request.user.id)
    view_sum = Counts.objects.filter(user=user_profile).aggregate(Sum('count'))
    intrests = Intrests.objects.filter(user=user_profile.user)
    view_count = Counts.objects.filter(user=user_profile).count()
    context = {
        'user': user_profile,
        'user_intrests': user_intrests,
        'view_count':view_count,
        'intrests':intrests,
        }
    return render(request,'user/profile.html',context)
    
def others_view_profile(request,id):
    user_profile = UserProfile.objects.get(user=id)
    intrests = Intrests.objects.filter(user=user_profile.user)
    view_sum = Counts.objects.filter(user=user_profile).aggregate(Sum('count'))
    # view_count = Counts.objects.filter(user=user_profile).count()
    current_user = Account.objects.get(id=request.user.id)
    if Counts.objects.filter(user=user_profile,viewed_by=current_user).exists():
        user_count = Counts.objects.get(user=user_profile,viewed_by=current_user)
        user_count.count = F('count')+ 1
        print(user_count.count,'(((((((((((((((((((((((((((((((((((((((((((((')
        user_count.save()
    else:
        Counts.objects.create(user=user_profile,viewed_by=current_user,count=1)
    context = {
        'user': user_profile,
        'intrests': intrests,
        }
    return render(request,'user/user_profile_others_view.html',context)
    
def user_profile_edit(request,id):
    user_profile = get_object_or_404(UserProfile,id=id)
    form = UserProfileForm(request.POST or None, instance=user_profile)
    if request.method == 'POST':
        form = UserProfileForm(request.POST,request.FILES,instance=user_profile)
        print(form.errors)
        if form.is_valid():
            form.save()
            messages.success(request,'Updated Your Details.....')
            return redirect('user_profile')
    context = {
        'form': form,
    }
    return render(request,'user/user_profile_edit.html',context)
    
def user_intrest_edit(request,id):
    intrests = Intrests.objects.filter(user=id).values_list('intrest',flat=True)
    category = list(JobCategory.objects.values_list('category_name',flat=True))
    form = IntrestEditForm(initial={'inrests': list(intrests)})
    if request.method == 'POST':
        form = IntrestEditForm(request.POST)
        if form.is_valid():
            intrestss =  form.cleaned_data.get("inrests")
            # this intrests taking from the user and adding to the intrest table 
            # if doesnot exist
            for intr in intrestss:
                if intr in category:
                    # for finding the deseleceted item 
                    category.remove(intr)
                if not Intrests.objects.filter(user=request.user,intrest=intr).exists():
                    Intrests.objects.create(user=request.user,intrest=intr)
            # This is for removing the existed element, if the user is not selected 
            # from the form,
            # while creating time the user is selected
            # updating time user deselected the item 
            for intrest in category:
                if Intrests.objects.filter(user=request.user,intrest=intrest).exists():
                    intrest = Intrests.objects.get(user=request.user,intrest=intrest)
                    intrest.delete()
            return redirect('user_profile')
    

    context = {
        'form': form,
    }
    return render(request,'user/intrest_form.html',context)
    
def profile_view_list(request,user_profile_id):
    profile_viewers = Counts.objects.filter(user=user_profile_id)
    print(profile_viewers,"%%%%%%%%%%%%%%%%%%%%%%%%")
    context = {
        'profile_viewers':profile_viewers,
    }
    
    return render(request,'user/profile_views_list.html',context)
   
def logout_view(request):
    ''' logout view of the user , '''
    
    logout(request)
    return redirect('home')
    

