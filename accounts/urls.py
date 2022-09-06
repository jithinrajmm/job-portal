from django.urls import path
from accounts import views


urlpatterns = [
    
    path('user_login/',views.user_login,name='user_login'),
    path('user_create/',views.UserCreation.as_view(),name='user_creation'),
    path('user_logout',views.logout_view,name='user_logout'),
    path('companies_register',views.company_register,name='company_register'),
    path('user_intrests/',views.user_intrests,name='user_intrests'),
    # this is used to view the profile by sel,user
    path('user_profile/',views.user_profile,name='user_profile'),
    path('user_profile_edit/<int:id>/',views.user_profile_edit,name='user_profile_edit'),
    path('user_intrest_edit/<int:id>/',views.user_intrest_edit,name='user_intrest_edit'),
    # this path for who all are viewed the proflies of the users
    path('profile_view_list/<int:user_profile_id>/',views.profile_view_list,name='profile_view_list'),
    
    
    # This is used to profile viewd by others
    path('others_view_profile/<int:id>/',views.others_view_profile,name='others_view_profile'),
    
    
    
]