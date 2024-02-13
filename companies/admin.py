from django.contrib import admin
from .models import Company, WorkerLevel, JobDetail

admin.site.register(Company)
admin.site.register(WorkerLevel)
admin.site.register(JobDetail)

