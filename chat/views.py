from django.shortcuts import render

from accounts.models import Account

# Create your views here.
def chat(request):
    user = Account.objects.get(id=request.user.id)
    context = {
        'user':user
    }
    return render(request,'chat.html',context)
