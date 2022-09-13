from django.urls import path
from chat import views


urlpatterns = [
    path('',views.chat,name='chat'),
    path('thread_creation/<int:user_id>/',views.thread_creation,name='thread_creation')
    ]