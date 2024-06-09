from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from dashboard.models import Task, TaskReview,TaskBid
from django.db.models.functions import Coalesce
from django.db.models import Count, Q, F

# Create your models here.


USER_TYPE = (
    ("freelancer","freelancer"),
    ("employer","employer"),
    ("admin","admin"),
)

SPECIALITY = [
    ("Solar Installation","Solar Installation"),
    ("Solar Maintenance","Solar Maintenance"),
    ("CCTV Installation","CCTV Installation"),
    ("CCTV Maintenance","CCTV Maintenance"),
    # CloudinaryField('image', default="hello.py")
]

class UserAdditionalInformation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPE, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    #profile_picture = models.ImageField(default="default.png")
    profile_picture = CloudinaryField('image', default="https://res.cloudinary.com/dmpxni4ku/image/upload/v1713334275/user-avatar-placeholder_dfzivc.png")
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class Freelancer(models.Model):
    user_additional_info = models.OneToOneField(UserAdditionalInformation, on_delete=models.CASCADE, related_name='freelancer_profile')
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    # Add any other fields specific to freelancers
    nationality = models.CharField(max_length=100, default="Nigeria")
    speciality = models.CharField(max_length=100, choices=SPECIALITY, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    lga = models.CharField(max_length=100, null=True, blank=True)
    tagline = models.CharField(max_length=250, null=True, blank=True)
    self_introduction = models.TextField(null=True, blank=True)
    minimum_pay = models.FloatField(null=True, blank=True)
    bookmark_freelancer = models.ManyToManyField("Freelancer", blank=True)
    bookmark_task = models.ManyToManyField(Task, blank=True)

    def total_tasks_done(self):
        return TaskBid.objects.filter(freelancer=self, accepted=True).count()

    def rehired_times(self):
        # Rehired times logic assumes that the freelancer is hired for the same task multiple times
        tasks = TaskBid.objects.filter(freelancer=self, accepted=True).values_list('task', flat=True).distinct()
        return tasks.count()

    def job_success(self):
        total_bids = TaskBid.objects.filter(freelancer=self).count()
        successful_bids = TaskBid.objects.filter(freelancer=self, accepted=True).count()
        return (successful_bids / total_bids * 100) if total_bids > 0 else 0

    def recommendation_rate(self):
        total_reviews = TaskReview.objects.filter(task__freelancer=self).count()
        recommended_reviews = TaskReview.objects.filter(task__freelancer=self, review__icontains="recommend").count()
        return (recommended_reviews / total_reviews * 100) if total_reviews > 0 else 0

    def on_time_rate(self):
        total_tasks = TaskBid.objects.filter(freelancer=self, accepted=True).count()
        on_time_tasks = TaskBid.objects.filter(freelancer=self, accepted=True, completed_on_time=True).count()
        return (on_time_tasks / total_tasks * 100) if total_tasks > 0 else 0

    def on_budget_rate(self):
        total_tasks = TaskBid.objects.filter(freelancer=self, accepted=True).count()
        on_budget_tasks = TaskBid.objects.filter(freelancer=self, accepted=True, completed_within_budget=True).count()
        return (on_budget_tasks / total_tasks * 100) if total_tasks > 0 else 0
    

class Employer(models.Model):
    user_additional_info = models.OneToOneField(UserAdditionalInformation, on_delete=models.CASCADE, related_name='employer_profile')
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    # Add any other fields specific to employers
    bookmark_freelancer = models.ManyToManyField(Freelancer, blank=True)
    bookmark_task = models.ManyToManyField(Task, blank=True)