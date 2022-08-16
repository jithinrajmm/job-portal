from django.db import models
from accounts.models import Companies

# Create your models here.
class Admin(models.Model):
    
    admin_name = models.CharField(max_length=100,unique=True)
    password = models.CharField(max_length=100)
    is_logedinn = models.BooleanField(default=False)

    @property
    def loginornot(self):
        return self.is_logedin


    def admin_authenticate(self,name,password):
        if self.admin_name == name and self.password == password:
            self.is_logedinn = True
            return True
        else:
            return False

    def admin_logout(self):
        self.is_logedin = False
    
    def __str__(self):
        return self.admin_name
        
class JobFair(models.Model):
    
    job_fair_name = models.CharField(max_length=100)
    conducted_date = models.DateField()
    company = models.ManyToManyField(Companies,through='JobFairRegister')
    
    # @property
    # def related_story_set(self):
    #    company_id_list = self.company.values_list("id", flat=True)
    #    jobfair = JobFair.objects.filter(company__id__in=company_id_list).exclude(id=self.id)
    #    print(company_id_list)
    #    for i in jobfair:
    #     print(i)
    #    return jobfair
       
    def __str__(self):
        return self.job_fair_name
    class Meta:
        ordering = ('-conducted_date',)
    
class JobFairRegister(models.Model):
    
    company = models.ForeignKey(Companies,on_delete=models.CASCADE)
    jobfair = models.ForeignKey(JobFair,on_delete=models.CASCADE)
    registerd_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.company.company_name
        
    class Meta:
        ordering = ('-registerd_date',)
    
    
    
