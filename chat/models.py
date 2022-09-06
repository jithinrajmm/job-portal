from django.db import models

from accounts.models import Account

class Thread(models.Model):
    ''' this model si store the two person 
    these two person can only chat with each other 
    ,these connection as thread , one thread that contain two person '''
    first_person = models.ForeignKey(Account,on_delete=models.CASCADE,null=True,blank=True,related_name='thread_first_person')
    second_person = models.ForeignKey(Account,on_delete=models.CASCADE,null=True,blank=True,related_name='thread_second_person')
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['first_person','second_person']
        
class ChatMessage(models.Model):
    # single thread can have multiple messages
    thread = models.ForeignKey(Thread,on_delete=models.CASCADE,related_name='chatmessage_thread')
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    # storing the messages of send_by user
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    