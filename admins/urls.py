from django.urls import path
from admins import views


urlpatterns = [
    path('',views.admin_home,name='admin_home'),
    path('login/',views.admin_login,name='admin_login'),
    # recruiter
    path('recruiter_activation/',views.recruiter_activation,name='recruiter_activation'),
    path('activate_recruiter/<int:pk>/',views.activate_recruiter,name='activate_recruiter'),
    path('recruiter_management/',views.recruiter_management,name='recruiter_management'),
    path('recruiter_management_activate/<int:pk>/',views.recruiter_management_activate,name='recruiter_management_activate'),
    # User
    path('user_management/',views.user_management,name = 'user_management'),
    path('user_active/<int:pk>/',views.user_active,name = 'user_active'),
    # Company
    path('company_management/',views.company_management,name='company_management'),
    path('spam_companies/',views.spam_companies,name='spam_companies'),
    path('list_users/<int:company_id>/',views.list_of_users,name='list_users'),
    path('spam_active_deactive/<int:company_id>/',views.spam_active_deactive,name='spam_active_deactive'),
    #category management
    path('category_list/',views.list_of_category,name='category_list'),
    path('add_category/',views.add_category,name='add_category'),
    path('edit_category/<int:pk>/',views.edit_category,name='edit_category'),
    path('delete_category/<int:pk>/',views.delete_category,name='delete_category'),
    # job fair management
    path('add_job_fair/',views.add_job_fair,name='add_job_fair'),
    path('list_job_fair/',views.list_job_fair,name='list_job_fair'),
    
    ]