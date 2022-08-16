from django.urls import path
from accounts import views


urlpatterns = [
    
    path('user_login/',views.user_login,name='user_login'),
    path('user_create/',views.UserCreation.as_view(),name='user_creation'),
    path('user_logout',views.logout_view,name='user_logout'),
    path('companies_register',views.company_register,name='company_register'),
    
]