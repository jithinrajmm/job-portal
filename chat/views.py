from django.shortcuts import render,redirect
# models
from chat.models import Thread
from accounts.models import Account
# Q expressions
from django.db.models import Q
# decorators
from django.contrib.auth.decorators import login_required

@login_required
def thread_creation(request,user_id):
    other_user = Account.objects.get(id=user_id)
    lookup = Q(first_person=request.user,second_person=other_user) | Q(first_person=other_user,second_person=request.user)
    
    if Thread.objects.filter(lookup).exists():
        pass
    else:
        Thread.objects.create(first_person=request.user,second_person=other_user)
    
    return redirect('chat')
    
@login_required   
def chat(request):
    
    threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread')
    user = Account.objects.get(id=request.user.id)
    context = {
        'user':user,
        'threads':threads
    }
    return render(request,'chat.html',context)
    # {% for chat in thread.chatmessage_thread.all %}
# class ThreadManager(models.Manager):
#     def by_user(self,**kwargs):
#         user = kwargs.get('user')
#         lookup = Q(first_person=user) | Q(second_person=user)
#         qs = self.get_queryset().filter(lookup).distinct()
#         return qs