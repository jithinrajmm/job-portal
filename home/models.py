from django.db import models
from accounts.models import Companies,Account

class JobCategory(models.Model):
    
    category_name = models.CharField(max_length=100)
    category_slug = models.SlugField(max_length=40)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.category_name
    
    
class Jobs(models.Model):
    
    JOB_TYPE = (
        ('ParTime','PRTIME'),
        ('FullTime','FULLTIME'),
        ('Intership','INTERNSHIP')
    )
    
    title = models.CharField(max_length=100)
    category = models.ForeignKey(JobCategory,on_delete=models.CASCADE)
    salary = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    company = models.ForeignKey(Companies,on_delete=models.CASCADE)
    job_type = models.CharField(max_length=100,choices=JOB_TYPE,default='FullTime')
    job_description = models.TextField()
    vacancies = models.IntegerField()
    experience = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True,null=True)
    updated = models.DateTimeField(auto_now=True,null=True)
    
    
    def __str__(self):
        return self.title
    class Meta:
        ordering = ('-created',)
        
def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.png', '.xlsx', '.xls']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')
        
class AppliedJobs(models.Model):
    ''' Application of job '''
    job = models.ForeignKey(Jobs,on_delete=models.CASCADE)
    user  = models.ForeignKey(Account,on_delete=models.CASCADE)
    resume = models.FileField(upload_to='pdfs/',validators=[validate_file_extension])
    selected = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('-created',)
    
    
class SpamCompanies(models.Model):
    ''' Spam comapnies '''
    
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    company = models.ForeignKey(Companies,on_delete=models.CASCADE)
    count = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    reason = models.TextField(max_length=200,null=True)
    
    class Meta:
        ordering = ('-created',)
    
    
    
    
