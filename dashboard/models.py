from django.db import models
from django.contrib.auth.models import User

# Create your models here.

TASK_CATEGORY = [
    ("Solar Installation", "Solar Installation"),
    ("Solar Maintenance", "Solar Maintenance"),
    ("CCTV Installation", "CCTV Installation"),
    ("CCTV Maintenance", "CCTV Maintenance"),
]


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=100)
    task_category = models.CharField(max_length=100, choices=TASK_CATEGORY)
    task_state = models.CharField(max_length=100)
    task_lga = models.CharField(max_length=100)
    task_min_pay = models.DecimalField(max_digits=10, decimal_places=2)
    task_max_pay = models.DecimalField(max_digits=10, decimal_places=2)
    task_type = models.CharField(max_length=20, choices=[("Fixed Price", "Fixed Price Project"), ("Hourly Rate", "Hourly Project")])
    task_description = models.TextField()
    task_deadline = models.DateTimeField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.task_name


class TaskFile(models.Model):
    task = models.ForeignKey(Task, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='task_files/')
    

class PrivateChat(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats_initiated')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats_received')

    def __str__(self):
        return f"{self.user1.username} - {self.user2.username}"


class PrivateMessage(models.Model):
    chat = models.ForeignKey(PrivateChat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content}"


class TaskBid(models.Model):
    freelancer = models.ForeignKey("accounts.Freelancer", on_delete=models.CASCADE)
    task = models.ForeignKey(Task, related_name='bids', on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    expected_delivery_time = models.IntegerField()
    expected_delivery_time_measurement = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)