from django.contrib import admin
from .models import Task, TaskBid, FreelancerNotification, PrivateChat, PrivateMessage

# Register your models here.

admin.site.register(Task)
admin.site.register(TaskBid)
admin.site.register(FreelancerNotification)
admin.site.register(PrivateChat)
admin.site.register(PrivateMessage)