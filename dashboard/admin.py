from django.contrib import admin
from .models import Task, TaskBid, FreelancerNotification

# Register your models here.

admin.site.register(Task)
admin.site.register(TaskBid)
admin.site.register(FreelancerNotification)