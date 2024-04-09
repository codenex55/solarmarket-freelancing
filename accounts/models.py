from django.db import models
from django.contrib.auth.models import User

# Create your models here.


USER_TYPE = (
    ("freelancer","freelancer"),
    ("employer","employer"),
    ("admin","admin"),
)

class UserAdditionalInformation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPE, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    profile_picture = models.ImageField(default="default.png")
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
