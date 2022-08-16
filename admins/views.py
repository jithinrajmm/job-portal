from unicodedata import name
from django.shortcuts import render,redirect
from django.contrib import messages
from django.db.models import Count

# forms
from admins.forms import AdminForm,CategoryForm,JobFairAddForm
# model 
from admins.models import Admin, JobFair
from accounts.models import Account, Companies
from home.models import Companies,SpamCompanies,JobCategory,Jobs
# error
from django.shortcuts import get_object_or_404
# decorators 
from admins.decorator import adminlogin,logout



# Create your views here.

def admin_home(request):
    if  not request.session.get('id'):
        return redirect('admin_login')
    return render(request,'admin_home.html')

@adminlogin   
def admin_login(request):
    form = AdminForm(request.POST or None)
    context = {
        'form': form,
    }
    if request.method =='POST':
        user_name = request.POST.get('admin_name')
        password1 = request.POST.get('password')
        if Admin.objects.filter(admin_name=user_name,password=password1).exists():
            user = Admin.objects.get(admin_name=user_name,password=password1)
            authenticated = user.admin_authenticate(user_name,password1)
            if authenticated:
                request.session['id']=user.id
                print(request.session.get('id'))
                return redirect('admin_home')
        else:
            messages.error(request, 'Not valid credentials')
        
    return render(request,'login.html',context)

@logout
def recruiter_activation(request):
    
    recruiters = Account.objects.filter(role='recruiter',is_recruiter=False)
    context = {
        'recruiters': recruiters,
    }
    return render(request,'recruiter_activate.html',context)
    
@logout   
def activate_recruiter(request,pk):
    recruiters = get_object_or_404(Account,pk=pk)
    
    recruiters.is_recruiter = not recruiters.is_recruiter
    recruiters.save()
    messages.success(request, 'Activated')
    
    return redirect('recruiter_activation')
    
@logout   
def recruiter_management(request):
    recruiter = Account.objects.filter(role='recruiter')
    
    context = {
        'recruiters': recruiter,
    }
    return render(request,'recruiter_management.html',context)
    
@logout    
def recruiter_management_activate(request,pk):
    recruiters = get_object_or_404(Account,pk=pk)
    recruiters.is_recruiter = not recruiters.is_recruiter
    recruiters.save()
    if recruiters.is_recruiter:
        messages.success(request, 'Activated')
    else:
        messages.error(request,' Deactivated ')
    
    return redirect('recruiter_management')
@logout   
def user_management(request):
    users = Account.objects.filter(is_recruiter=False,is_superuser=False)
    context = {
        'users': users
    }
    return render(request,'user_management.html',context)
@logout   
def user_active(request,pk):
    user = get_object_or_404(Account,pk=pk)
    user.is_active = not user.is_active
    user.save()
    return redirect('user_management')
    
@logout   
def company_management(request):
    companies = Companies.objects.all()
    
    context = {
        'companies': companies,
    }
    
    return render(request,'company/company_manage.html',context)
@logout    
def spam_companies(request):
    spam = SpamCompanies.objects.values('company').annotate(count_c= Count('company'))
    spamed_companies = []
    for company in spam:
        if company['count_c'] > 3:
            company = Companies.objects.get(id=company['company'])
            spamed_companies.append(company)            
    context = {
       'spam_companies': spamed_companies, 
    }  
    return render(request,'company/spam_companies.html',context) 

@logout
def list_of_users(request,company_id):
    ''' this view is showing the users who marked the spams 
    from the companies we can take the user'''
    companies = SpamCompanies.objects.filter(company=company_id)
    context = {
        'companies':companies,
    }
    return render(request,'company/list_spam_users.html',context)
    
@logout
def spam_active_deactive(request,company_id):
    
    company = Companies.objects.get(pk=company_id)
    company.spam = not company.spam
    company.save()
    if company.spam:
        messages.error(request,'Spammed the compnay')
        return redirect('spam_companies')
    else:
        messages.success(request,'removed from the span list')
        return redirect('spam_companies')

#CATEGORY        
@logout       
def list_of_category(request):
    
    job_category = JobCategory.objects.all()
    context = {
        'job_category': job_category,
    }
    return render(request,'category/category_list.html',context)

def add_category(request):
    form = CategoryForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid:
            value = form.save(commit=False)
            value.category_slug = (form.cleaned_data['category_name']).replace(' ','')
            value.save()
            return redirect('category_list')
    button_text = 'ADD'
    context = {
        'form': form,
        'button_text': button_text,
    }
    
            
    return render(request,'category/category_add.html',context)

def edit_category(request,pk):
    
    category = get_object_or_404(JobCategory,id=pk)
    form = CategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        value = form.save(commit=False)
        value.category_slug = (form.cleaned_data['category_name']).replace(' ','')
        value.save()
        return redirect('category_list')
    context = {
        'form': form,
    }
    return render(request,'category/category_add.html',context)

def delete_category(request,pk):
    category = get_object_or_404(JobCategory,id=pk)
    category.delete()
    return redirect('category_list')

#JOB FAIR MANAGEMENT
def list_job_fair(request):
    
    job_fairs = JobFair.objects.all()
    context = {
        'job_fairs': job_fairs,
    }
    return render(request,'jobfair/job_fair_list.html',context)
    
def add_job_fair(request):
    form = JobFairAddForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('admin_home')
        
    context = {
        'form':form
    }
    
    return render(request,'jobfair/add_jobfair.html',context)

    
        
    
    
    
