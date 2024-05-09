from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from dashboard.models import Task

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

class Employer(models.Model):
    user_additional_info = models.OneToOneField(UserAdditionalInformation, on_delete=models.CASCADE, related_name='employer_profile')
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    # Add any other fields specific to employers
    bookmark_freelancer = models.ManyToManyField(Freelancer, blank=True)
    bookmark_task = models.ManyToManyField(Task, blank=True)