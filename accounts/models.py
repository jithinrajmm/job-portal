
from django.db import models

# Create your models here.
####################################
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.utils import timezone
import random
from django.core.validators import RegexValidator
# for countries feild 
from django_countries.fields import CountryField

# for validation error phone number
from django.core.exceptions import ValidationError

from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe

####################################


class CustomUserManager(BaseUserManager):
    
    def create_user(self,first_name,last_name,username,email,password,**other_fields):
        if not email:
            raise ValueError('The Email is mandatory')
        if not username:
            raise ValueError('The username is mandatory')

        user = self.model(
            email= self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,**other_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,first_name,last_name,username,email,password,**other_fields):

        other_fields.setdefault('is_staff',True)
        other_fields.setdefault('is_superuser',True)
        other_fields.setdefault('is_active',True)
        other_fields.setdefault('is_admin',True)
        
    #  this is and validation checkup while creation method
        if other_fields.get('is_staff') is not True:
            raise ValueError('Super user is_staff must be True')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('is_superuser must set to True')
        if other_fields.get('is_active') is not True:
            raise ValueError('is_active must be set to True')
        if other_fields.get('is_admin') is not True:
            raise ValueError('is_admin must be set to True')

        return self.create_user(first_name,last_name,username,email,password,**other_fields)
    

class Account(AbstractBaseUser,PermissionsMixin):
    ''' This is the user models which created the help of abstract Base User , we need to 
    write every things from the scratch in this AbstractBaseUser '''
    
    # Choce fiedls creation
    
    ROLE = (
        ('applicant','APPLICANT'),
        ('recruiter','RECRUITER')
        )
    

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=100,unique=True)
    email = models.EmailField(max_length=100,unique=True)
    phone = models.CharField(max_length=20)

    # extra added tta 
    #required 
    role = models.CharField(max_length=100,choices=ROLE,default='Applicant')
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_recruiter = models.BooleanField(default=False)

    # Specified that all objects for the class come from the CustomUserManager
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name']

    def __str__(self):
        return self.email
        
    # choice feild
    
def validate_mobile_len(value):
    if len(value)<10 or len(value)>12:
        raise ValidationError(
            _('should 10 numbers'),
            params={'value': value},
        )
    
def validate_comas(value):
    if ',' not in value:
        raise ValidationError(
            _('place should be separated with comas'),
            params={'value': value},
        )

class Companies(models.Model):

    company_name = models.CharField(max_length=100)
    email = models.EmailField()
    contact_number = models.CharField(max_length=12,validators=[validate_mobile_len])
    image = models.ImageField(upload_to='companies/')
    country = CountryField()
    places = models.CharField(max_length=200,help_text= mark_safe(_(
            '<h6 style="color:white">place should be separated by coma</h6>'
        )),validators=[validate_comas])
    recruiter = models.OneToOneField(Account,on_delete=models.CASCADE)
    link = models.URLField(max_length=200,null=True)
    spam = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.company_name
    class Meta:
        ordering = ('-updated',)
        
class Intrests(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    intrest = models.CharField(max_length=100)
    def __str__(self):
        return self.user.username
        
class UserProfile(models.Model):

    user = models.OneToOneField(Account,on_delete=models.CASCADE,related_name='profile')
    profile_pic = models.ImageField(upload_to='profile/',max_length=500,default='profile/avatar.png')
    first_name = models.CharField(max_length=50,null=True)
    last_name = models.CharField(max_length=50,null=True)
    username = models.CharField(max_length=100,null=True)
    email = models.EmailField(max_length=100,null=True)
    phone = models.CharField(max_length=15, validators=[RegexValidator(r'^\d{1,15}$')])
    country = models.CharField(max_length=50,null=True)
    state = models.CharField(max_length=50,null=True)
    city = models.CharField(max_length=50,null=True)
    

    def __str__(self):
        return self.user.username

#for displaying the count of the user which viewed the profies       
class Counts(models.Model):
    
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    viewed_by = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    count = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True,null=True)
    
    def __str__(self):
        return self.user.username + str(self.count)
        