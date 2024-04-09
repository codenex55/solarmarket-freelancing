from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class TaskCategory(models.Model):
    category = models.CharField(max_length=255)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=100)
    task_category = models.CharField(max_length=100)
    task_location = models.CharField(max_length=100)
    task_min_pay = models.DecimalField(max_digits=10, decimal_places=2)
    task_max_pay = models.DecimalField(max_digits=10, decimal_places=2)
    task_type = models.CharField(max_length=20, choices=[("Fixed Price", "Fixed Price Project"), ("Hourly Rate", "Hourly Project")])
    task_skills = models.CharField(max_length=255)
    task_description = models.TextField()
    task_images = models.ImageField(upload_to='task_images/')
    task_deadline = models.DateTimeField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.task_name
    

class EmployerBookmarked(models.Model):
    user = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE)
    bookmarked_freelancer = models.ManyToManyField(User, related_name="bookmarked_freelancer")
    timestamp = models.DateTimeField(auto_now_add=True)

    

# class JobCategory(models.Model):
#     category = models.CharField(max_length=255)
#     updated = models.DateTimeField(auto_now=True)
#     timestamp = models.DateTimeField(auto_now_add=True)


# class Task(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     task_name = models.CharField(max_length=100)
#     task_category = models.CharField(max_length=100)
#     task_location = models.CharField(max_length=100)
#     task_min_pay = models.DecimalField(max_digits=10, decimal_places=2)
#     task_max_pay = models.DecimalField(max_digits=10, decimal_places=2)
#     task_type = models.CharField(max_length=20, choices=[("fixed_price", "Fixed Price Project"), ("hourly", "Hourly Project")])
#     task_skills = models.CharField(max_length=255)
#     task_description = models.TextField()
#     task_images = models.ImageField(upload_to='task_images/')
#     task_deadline = models.DateTimeField()
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.task_name

