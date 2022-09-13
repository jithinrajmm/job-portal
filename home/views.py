
##############################################
from django.shortcuts import redirect, render
from django.db.models import Count
from django.urls import reverse_lazy,reverse
# models
from home.models import AppliedJobs, Jobs,JobCategory,SpamCompanies
from accounts.models import Account,Companies, Intrests
from admins.models import JobFair,JobFairRegister
# error
from django.shortcuts import get_object_or_404
# messages
from django.contrib import messages
# for viewing the whole items, class based view
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
# this is for the djanog filter views
from django_filters.views import FilterView
# job filter
from home.filter import JobsFilter
# for updating the existing value in the database
# its called query expression
from django.db.models import F,Q
# decorator
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
# forms 
from home.forms import JObAddForm,ApplyJobForm,SpamCompaniesForm,JobEditForm
from home.forms import JobFairRegisterForm,JobFairSearch
import datetime
# for the iframe from same origin
from django.views.decorators.clickjacking import xframe_options_sameorigin
# date and time
from datetime import timedelta
from django.utils import timezone




# All the recruiter and user view start here 
def home(request):
    count = request.GET.get('intial_value')

    if not count:
        count = 1
    else:
        count = int(count)+1 
         
    categories = JobCategory.objects.all()[:5] 
    jobs = Jobs.objects.all()[:count]
    job_count = Jobs.objects.all().count()
    companies = Companies.objects.all()[:6]
    context = {
        'categories': categories,
        'companies': companies,
        'jobs': jobs,
        'count': int(count),
        'job_count': job_count,
        
    }
    return render(request,'home.html',context)
    
# RECRUITER
@login_required
def job_post(request):
    form = JObAddForm(request=request)
    context = {
        'form': form,
    }
    if request.method == "POST":
        form = JObAddForm(data = request.POST,request=request)
        
        if form.is_valid():
            job = form.save(commit=False)
            category = form.cleaned_data['category_']
            
            if JobCategory.objects.filter(category_name__exact=category).exists():
                category = JobCategory.objects.get(category_name = category)
                job.category = category
                job.save()
            else:
                category_slug = category.replace(' ',"")
                new_job_category = JobCategory.objects.create(category_name=category,
                category_slug=category_slug)
                new_job_category.save()
                job.category = new_job_category
                job.save()

            return redirect('job_list')
    
    return render(request,'recruiter/add_job.html',context)
    
# USER 
# ####################################################################################### 
class JobList(FilterView):
    '''For listing the all jobs '''
    model = Jobs
    template_name = 'home/job_list.html'
    context_object_name = 'jobs'
    filterset_class = JobsFilter 
    paginate_by = 4
    
    def get_queryset(self):    
        qs = super().get_queryset()
        if self.request.user.is_authenticated:
            qs = super().get_queryset()
            if self.request.user.is_recruiter:
                return qs
            intrests = [intrest.intrest for intrest in Intrests.objects.filter(user=self.request.user)]
            qs = qs.filter(category__category_name__in = intrests)
            return qs.exclude(id__in=[ i.job.id for i in AppliedJobs.objects.all()])
        else:
            return qs

    def get_context_data(self,**kwargs):
        context = super(JobList,self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['applied'] = AppliedJobs.objects.filter(user=self.request.user) 
        countries = Jobs.objects.values('company').annotate(c_count=Count('company'))

        for i in countries:
            company = Companies.objects.get(id=i['company'])
            i['company'] = company

        context['countries'] = countries
        context['categories'] = JobCategory.objects.all()
        return context
    
class CompanyList(ListView):
    ''' For listing the all companies '''
    model = Companies
    template_name = 'home/companies.html'
    context_object_name = 'companies'
    paginate_by = 10
    def get_queryset(self):
        qs =  super().get_queryset()
        return qs.filter(spam=False)
    
class CompanyDetail(DetailView):
    ''' For viewing the single view of the companies '''
    model = Companies
    pk_url_kwarg = 'pk'
    template_name = 'home/single_company.html'
    context_object_name='company'

@method_decorator(login_required,name='dispatch')  
class JobApply(View):
    ''' For applying the job , for users''' 
    def get(self,request,job_id):
        try:
            job = Jobs.objects.get(id=job_id)
        except Jobs.DoesNotExist:
            job = None
        form = ApplyJobForm()
        
        context = {
            'form': form,
            'job': job,
        }
        return render(request,'user/job_apply.html',context)
    
    def post(self,request,job_id):
        try:
            job = Jobs.objects.get(id=job_id)
        except Jobs.DoesNotExist:
            job = None
        form = ApplyJobForm(request.POST,request.FILES)
        if form.is_valid():
            instance = AppliedJobs(resume=request.FILES['resume'])
            instance.user = request.user
            instance.job = job
            instance.save()
            messages.success(request,'your application success')
            return redirect('job_list')
            
@method_decorator(login_required,name='dispatch')            
class UserAppliedJobs(ListView):
    ''' user applied job list according to user'''
    model = AppliedJobs
    template_name = 'user/applied_job.html'
    context_object_name = 'applied_jobs'
    paginate_by = 10
    def get_queryset(self):
        qs = super(UserAppliedJobs,self).get_queryset()
        return qs.filter(user=self.request.user)
        
    def get(self,request,*args,**kwargs):
        if request.GET.get('date'):
            date = request.GET.get('date')
            query_set = self.get_queryset() 
            self.object_list = query_set.filter(created__date=date) 
            context = self.get_context_data()
            return self.render_to_response(context)
  
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return self.render_to_response(context)

@login_required       
def unapply_job(request,applied_job_id):
    ''' deleting the applied jobs '''
    applied_job = get_object_or_404(AppliedJobs,id = applied_job_id)
    applied_job.delete()
    return redirect('user_applied_jobs')
    

class RecruitersList(ListView):
    ''' This is for the recruiterlist ''' 
    model = Account
    template_name = 'home/list_of_recruiters.html'
    context_object_name = 'recruiters'
    paginate_by = 10
    
    def get_queryset(self):
        qs = super().get_queryset() 
        return qs.filter(is_recruiter=True)
        
    def get_context_data(self,**kwargs):
        jobs = Jobs.objects.values('company').annotate(ccount = Count('company'))
        companies_id=[i['company']  for i in jobs]
        jobs_objects = Companies.objects.filter(pk__in = companies_id)
        print(jobs_objects)
        for i in range(len(jobs)):
            jobs[i]['company_name'] = jobs_objects[i].company_name
        
        
        context = super(RecruitersList,self).get_context_data(**kwargs)
        context['jobs'] = jobs 
        return context
        
    def get(self,request,*args,**kwargs):
        if request.GET.get('company'):
            company = request.GET.get('company')
            recruiters_list = Companies.objects.values_list('recruiter',flat=True).filter(company_name=company)
            # print(intrests_users) here we are taking the users based on the 
            # intrests choosed from the front end
            query_set = self.get_queryset() 
            self.object_list = query_set.filter(id__in=recruiters_list) 
            context = self.get_context_data()
            return self.render_to_response(context)
                    
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return self.render_to_response(context)
       
class ApplicantsList(ListView):
    ''' this is for the list of user from the recruiter side'''
    model = Account
    template_name = 'home/applicants_list.html'
    context_object_name = 'applicants'
    paginate_by = 10
    
    def get_queryset(self):
        qs = super().get_queryset() 
        return qs.filter(role='applicant')
        
    def get_context_data(self,**kwargs):
        context = super(ApplicantsList,self).get_context_data(**kwargs)
        category = Intrests.objects.values('intrest').annotate(intrest_count=Count('intrest'))
        user = Account.objects.values().annotate(intrests_count=(Count('intrests')))
        context['category'] = category
        return context
        
    def get(self,request,*args,**kwargs):
        
        if request.GET.get('categ'):
            category = request.GET.get('categ')
            intrests_users = Intrests.objects.values_list('user',flat=True).filter(intrest=category)
            # print(intrests_users) here we are taking the users based on the 
            # intrests choosed from the front end
            query_set = self.get_queryset() 
            self.object_list = query_set.filter(id__in=intrests_users) 
            context = self.get_context_data()
            return self.render_to_response(context)
            
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return self.render_to_response(context)

        
        
class JobFairList(ListView):
    '''To display List of jobfar to user and recruiters'''
    model = JobFair
    template_name='user/job_fairs_list.html'
    context_object_name = 'job_fairs'
    
    def get_queryset(self):
        qs = super().get_queryset()
        values = list(JobFairRegister.objects.values_list('jobfair',flat=True))
        values = list(set(values))
        qs = qs.filter(id__in = values)
        return qs
        
    def get(self,request,*args,**kwargs):
        
        if request.GET.get('date') or request.GET.get('place'):
            
            if request.GET.get('date'):
                date = request.GET.get('date')
                query_set = self.get_queryset() 
                self.object_list = query_set.filter(conducted_date=date) 
                context = self.get_context_data()
                return self.render_to_response(context)
                        
            if request.GET.get('place'):
                place = request.GET.get('place')
                query_set = self.get_queryset()
                self.object_list = query_set.filter(Q(location__icontains=place)|Q(job_fair_name__icontains=place))
                context = self.get_context_data()
                return self.render_to_response(context)
            
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return self.render_to_response(context)

##############################################################################################
# RECRUITER   
@method_decorator(login_required,name='dispatch') 
class ListPostedJobs(ListView):
    '''For listing the Whole posted jobs related by the Recruiter'''
    model = Jobs
    template_name = 'recruiter/posted_jobs.html'
    context_object_name='jobs'
    
    def get_queryset(self):
        # if self.request.GET.get('job'):
        # original qs
        qs = super().get_queryset() 
        # changing the query set related to the user in the companies table
        # company is the foreign key relations from the Jobs table
        # recruiter is the feild in the Companies table
        return qs.filter(company__recruiter=self.request.user.id)

@method_decorator(login_required,name='dispatch') 
class UpdateJob(UpdateView):
    '''For updating the jobs posted by the recruiter's'''
    model = Jobs
    template_name = 'recruiter/edit_job.html'
    form_class = JobEditForm
    success_url = reverse_lazy('posted_job')
    
    def get_form_kwargs(self):
        """ Passes the request object to the form class.
         This is necessary to only display members that belong to a given user"""
        kwargs = super(UpdateJob, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
        
# for deleting the job
@login_required
def delete_job(request,job_id):
    job = Jobs.objects.get(id=job_id)
    job.delete()
    return redirect(reverse('posted_job'))

@method_decorator(login_required,name='dispatch')       
class JobApplications(ListView):
    """ This view used to showing the applications of applicant"""
    model= AppliedJobs
    template_name = 'recruiter/user_applied_job.html'
    context_object_name = 'applications'
    
    def get_queryset(self):
        qs = super().get_queryset() 
        return qs.filter(job__company__recruiter=self.request.user)
        
    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        category = [i.job.category.category_name for i in AppliedJobs.objects.filter(job__company__recruiter=self.request.user)]
        category = list(set(category))
        context['category'] = category
        return context
        
    def get(self,request,*args,**kwargs):
        if request.GET.get('category'):
            category = request.GET.get('category')
            # category = JobCategory.objects.get(category_name=category)
            print(category,'*'*100)
            query_set = self.get_queryset() 
            self.object_list = query_set.filter(job__category__category_name=category) 
            context = self.get_context_data()
            return self.render_to_response(context)
            
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return self.render_to_response(context)
        
decorators = [login_required,xframe_options_sameorigin]
@method_decorator(decorators, name='dispatch')      
class AppliedJobDetailView(DetailView):
    model = AppliedJobs
    template_name = 'recruiter/applied_job_detail.html'
    context_object_name = 'applied_job'
    
    def get_queryset(self):
        applied_job = get_object_or_404(AppliedJobs,pk=self.kwargs['pk'])
        applied_job.viewed = True
        applied_job.save()
        qs = super().get_queryset()
        return qs
        
    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        return context
    
        
@method_decorator(login_required,name='dispatch')         
class SpamCompany(View):
    ''' for spaming companies by users, for adding the reason of spaming'''
    def get(self,request,company_id):
        company = get_object_or_404(Companies,pk=company_id)
        form = SpamCompaniesForm()
        context = {
            'form': form,
            'company': company,
        }
        return render(request,'home/spam_reason_form.html',context)
            
    def post(self,request,company_id):
        
        user = self.request.user
        company = get_object_or_404(Companies,pk=company_id)
        form = SpamCompaniesForm(request.POST)
        if form.is_valid():
            reason = form.cleaned_data['reason']
            if SpamCompanies.objects.filter(user=user,company=company).exists():
                messages.error(request,'You are already marked as spam')
                return redirect('company_detail',pk=company_id)
            else:
                spam_companies = SpamCompanies.objects.create(user=user,company=company,count=1,reason=reason)
                spam_companies.save()
                messages.error(request,'Marked As Spam')
                return redirect('company_detail',pk=company_id)


#JOB FAIR'S 
@login_required
def register_job_fair(request):
    form = JobFairRegisterForm(request=request)
    if request.method == 'POST':
        form = JobFairRegisterForm(request.POST,request=request)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {
        'form': form,
    }
    return render(request,'recruiter/register_job_fair.html',context)


@method_decorator(login_required,name='dispatch')  
class RegisterdJobFairsList(ListView):
    ''' For showing the registerd job fairs related to the recruiter'''
    model= JobFairRegister
    template_name = 'recruiter/jobfair_registerd_list.html'
    context_object_name = 'jobfairs'
    
    def get_queryset(self):
        qs = super().get_queryset() 
        qs = JobFairRegister.objects.filter(company__recruiter=self.request.user.id)
        return qs  
    
    def get(self,request,*args,**kwargs):
        print(request.GET)
        if request.GET.get('date'):
            date = request.GET.get('date')
            query_set = self.get_queryset() 
            self.object_list = query_set.filter(jobfair__conducted_date=date) 
            context = self.get_context_data()
            return self.render_to_response(context)
            
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return self.render_to_response(context)
        

      
class ListJobFairs(ListView):
    ''''''
    model = JobFair
    template_name = 'recruiter/list_of_job_fairs.html'
    context_object_name = 'job_fairs'
    
    def get_queryset(self):
        company = get_object_or_404(Companies,recruiter=self.request.user.id)
        today = datetime.datetime.today()
        qs = super().get_queryset() 
        qs = JobFair.objects.filter(conducted_date__gte=today)
        qs = qs.filter(~Q(company__id=company.id))
        return qs
        
    def get(self,request,*args,**kwargs):
        if request.GET.get('date'):
            date = request.GET.get('date')
            query_set = self.get_queryset() 
            self.object_list = query_set.filter(conducted_date=date) 
            context = self.get_context_data()
            return self.render_to_response(context)
            
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return self.render_to_response(context)

@login_required        
def apply_for_job_fair(request,job_fair_id):
    company = get_object_or_404(Companies,recruiter=request.user.id)
    if JobFairRegister.objects.filter(company=company,jobfair=job_fair_id).exists():
        messages.error(request,'already registerd this company')
    else:
        jobfair = get_object_or_404(JobFair,id=job_fair_id)
        jobfair_register = JobFairRegister.objects.create(company=company,jobfair=jobfair)
        jobfair_register.save()
        return redirect('register_job_fair_list')
        
@login_required
def delete_registerd_job_fair(request,job_fair_id):
    registerd_job = JobFairRegister.objects.get(id=job_fair_id)
    registerd_job.delete()
    return redirect('register_job_fair_list')
    

    
    

    
                


        
    
        

    
      