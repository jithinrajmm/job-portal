from django.contrib import admin
from home.models import Jobs,JobCategory,AppliedJobs,SpamCompanies

# Register your models here.
admin.site.register(Jobs)
admin.site.register(JobCategory)
admin.site.register(AppliedJobs)
admin.site.register(SpamCompanies)

