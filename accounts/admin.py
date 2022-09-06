from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import Account,Companies,UserProfile,Counts,Intrests

# Register your models here.
class AccountAdmin(UserAdmin):
    
    model = Account
    ordering = ('-date_joined',)
    list_display = ('username','email','first_name','last_name','is_active','is_staff','is_superuser','date_joined','password')


    # this is set to the user individuals displaying
    fieldsets = (
        (None,{'fields':('email','first_name','username','phone','role')}),
        ('Permission',{'fields':('is_active','is_staff','is_recruiter','is_superuser','is_admin')}),
        ('Personal',{'fields':('last_name',)})
    )

    add_fieldsets = (
        ('PLEASE ENTER YOUR CREDENTIALS ',{'classes':('wide',),'fields':('email','username','password1','password2')}),
    )
    readonly_fields = ("date_joined","last_login")

admin.site.register(Account,AccountAdmin)
admin.site.register(Companies)
admin.site.register(UserProfile)
admin.site.register(Counts)
admin.site.register(Intrests)
