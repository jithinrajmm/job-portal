from itertools import count
from re import search
from turtle import color
from unicodedata import name
from django.shortcuts import render,redirect
from django.contrib import messages
from django.db.models import Count

# forms
from admins.forms import AdminForm,CategoryForm,JobFairAddForm
# model 
from admins.models import Admin, JobFair, JobFairRegister
from accounts.models import Account, Companies
from home.models import Companies,SpamCompanies,JobCategory,Jobs
# error
from django.shortcuts import get_object_or_404
# decorators 
from admins.decorator import adminlogin,logout
from django.views.decorators.cache import never_cache
# Q() objects
from django.db.models import Q
# pagination
from django.core.paginator import Paginator
# datetime
import datetime
import json
import random




# Create your views here.
@never_cache
@logout
def admin_home(request):
    if  not request.session.get('id'):
        return redirect('admin_login')
    today = datetime.date.today()
    recruiter = Account.objects.filter(role='recruiter').count()
    recruiter_new = Account.objects.filter(role='recruiter',is_recruiter=False).count()
    users = Account.objects.filter(is_recruiter=False,is_superuser=False).count()
    todays_jobs = Jobs.objects.filter(created__date=today).count()
    total_jobs = Jobs.objects.all().count()
    job_fair = JobFair.objects.filter(conducted_date__gte=today).count()
    category_group = Jobs.objects.values('category__category_name').annotate(count = Count('category')).order_by('-count')[:5]
    countries = [obj['company__country'] for obj in Jobs.objects.values('company__country').annotate(count=Count('company'))]
    colors = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(len(countries))]
    countries_count = [i['count'] for i in Jobs.objects.values('company__country').annotate(count=Count('company'))]
    context = {
        'recruiter':recruiter,
        'recruiter_new':recruiter_new,
        'todays_jobs':todays_jobs,
        'total_jobs':total_jobs,
        'users':users,
        'category_group':category_group,
        'job_fair':job_fair,
        'countries':json.dumps(countries),
        'colors': json.dumps(colors),
        'countries_count':json.dumps(countries_count),
        
    }
    return render(request,'admin_home.html',context)

@adminlogin  
@never_cache 
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
@never_cache
def recruiter_activation(request):
    recruiters = Account.objects.filter(role='recruiter',is_recruiter=False)
    context = {
        'recruiters': recruiters,
    }
    return render(request,'recruiter_activate.html',context)
    
@logout   
@never_cache
def activate_recruiter(request,pk):
    recruiters = get_object_or_404(Account,pk=pk)
    recruiters.is_recruiter = not recruiters.is_recruiter
    recruiters.save()
    messages.success(request, 'Activated')
    return redirect('recruiter_activation')
    
@logout  
@never_cache 
def recruiter_management(request):
    recruiter = Account.objects.filter(role='recruiter')
    search = request.GET.get('recruiters')
    search_item = False
    if search:
        recruiter = Account.objects.filter(role='recruiter')
        recruiter = recruiter.filter(Q(first_name__icontains=search)| 
        Q(last_name__icontains=search)| Q(username__icontains=search)| Q(email__icontains=search))
        search_item = True
    paginator = Paginator(recruiter,10)
    page_number = request.GET.get('page')
    recruiter = paginator.get_page(page_number)
    context = {
        'recruiters': recruiter,
        'search_item':search_item,
    }
    return render(request,'recruiter_management.html',context)
    
@logout  
@never_cache  
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
@never_cache 
def user_management(request):
    users = Account.objects.filter(is_recruiter=False,is_superuser=False)
    search = request.GET.get('user')
    search_item = False
    if search:
        users = Account.objects.filter(is_recruiter=False,is_superuser=False)
        users = users.filter(Q(first_name__icontains=search)| 
        Q(last_name__icontains=search)| Q(username__icontains=search)| Q(email__icontains=search))
        search_item = True
    paginator = Paginator(users,5)
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)
        
    context = {
        'users': users,
        'search_item':search_item,
    }
    return render(request,'user_management.html',context)
    
@logout  
@never_cache 
def user_active(request,pk):
    user = get_object_or_404(Account,pk=pk)
    user.is_active = not user.is_active
    user.save()
    return redirect('user_management')
    
@logout 
@never_cache  
def company_management(request):
    companies = Companies.objects.all()
    paginator = Paginator(companies,10)
    page_number = request.GET.get('page')
    companies = paginator.get_page(page_number)
    
    context = {
        'companies': companies,
    }
    
    return render(request,'company/company_manage.html',context)
    
@logout  
@never_cache  
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
@never_cache
def list_of_users(request,company_id):
    ''' this view is showing the users who marked the spams 
    from the companies we can take the user'''
    companies = SpamCompanies.objects.filter(company=company_id)
    context = {
        'companies':companies,
    }
    return render(request,'company/list_spam_users.html',context)
    
@logout
@never_cache
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
@never_cache      
def list_of_category(request):
    
    job_category = JobCategory.objects.all()
    search = request.GET.get('category')
    search_reset = False
    if search:
        job_category = JobCategory.objects.filter(category_name__icontains=search)
        search_reset = True
    paginator = Paginator(job_category,4)
    page_number = request.GET.get('page')
    job_category = paginator.get_page(page_number)
    context = {
        'job_category': job_category,
        'search_reset':search_reset,
    }
    return render(request,'category/category_list.html',context)

@logout 
@never_cache
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
    
@logout 
@never_cache
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

@logout 
@never_cache
def delete_category(request,pk):
    category = get_object_or_404(JobCategory,id=pk)
    category.delete()
    return redirect('category_list')

#JOB FAIR MANAGEMENT
@logout 
@never_cache
def list_job_fair(request):
    job_fairs = JobFair.objects.all()
    search = request.GET.get('job_fair')
    search_reset = False
    if search:
        job_fairs = JobFair.objects.filter(job_fair_name__icontains=search)
        search_reset = True
    paginator = Paginator(job_fairs,10)
    page_number = request.GET.get('page')
    job_fairs = paginator.get_page(page_number)
    
    context = {
        'job_fairs': job_fairs,
        'search_reset':search_reset
    }
    return render(request,'jobfair/job_fair_list.html',context)

@logout
@never_cache     
def add_job_fair(request):
    form = JobFairAddForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('list_job_fair')   
    context = {
        'form':form
    }
    return render(request,'jobfair/add_jobfair.html',context)

@logout 
@never_cache  
def job_fair_delete(request,job_fair_id):
    
    job_fair = get_object_or_404(JobFair,id = job_fair_id)
    job_fair.delete()
    return redirect('list_job_fair')

@logout 
@never_cache   
def companies_joined_job_fair(request,job_fair_id):
    """ is used to view the all companies which registerd in the 
    job fair """
    companies = JobFairRegister.objects.filter(jobfair__id=job_fair_id)
    
    context = {
        'companies': companies,
    }
    return render(request,'jobfair/registered_companies.html',context)
 
@logout  
@never_cache  
def edit_job_fair(request,job_fair_id):
    
    job_fair = get_object_or_404(JobFair,id = job_fair_id)
    form = JobFairAddForm(request.POST or None, instance=job_fair)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('list_job_fair')   
    context = {
        'form':form
    }
    return render(request,'jobfair/add_jobfair.html',context)
    
def admin_logout(request):
    del request.session['id']
    return redirect('admin_login')
        
    
    
    
