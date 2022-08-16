
from django.urls import path
from home import views


urlpatterns = [
    path('',views.home,name='home'),
    # job details
    path('job_post/',views.job_post,name='job_post'),
    path('job_list/',views.JobList.as_view(),name='job_list'),
    # comapny details
    path('companies_list/',views.CompanyList.as_view(),name='companies_list'),
    path('company_detail/<int:pk>/',views.CompanyDetail.as_view(),name='company_detail'),
    path('list_of_recruiters/',views.RecruitersList.as_view(),name='list_of_recruiters'),
    path('spam_company/<int:company_id>/',views.SpamCompany.as_view(),name='spam_company'),
    # recruiter
    path('posted_job/',views.ListPostedJobs.as_view(),name='posted_job'),
    path('job_applications/',views.JobApplications.as_view(),name='job_applications'),
    path('job_update/<int:pk>/',views.UpdateJob.as_view(),name='job_update'),
    path('job_delete/<int:job_id>/',views.delete_job,name='delete_job'),
   
       #job fair register
    path('register_job_fair/',views.register_job_fair,name='register_job_fair'),
    path('apply_job_fair/<int:job_fair_id>/',views.apply_for_job_fair,name='apply_job_fair'),
    path('list_of_job_fair/',views.ListJobFairs.as_view(),name='list_of_job_fair'),
    path('register_job_fair_list/',views.RegisterdJobFairsList.as_view(),name='register_job_fair_list'),
    path('delete_registerd_job_fair/<int:job_fair_id>/',views.delete_registerd_job_fair,name='delete_registerd_job_fair'),
    
    # user
    path('apply_job/<int:job_id>/',views.JobApply.as_view(),name='apply_job'),
    path('job_fair_list/',views.JobFairList.as_view(),name='job_fair_list'),
    

     
]