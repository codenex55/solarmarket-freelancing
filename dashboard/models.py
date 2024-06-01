from django.db import models
from django.contrib.auth.models import User
import uuid

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
    accepted_bid = models.OneToOneField('TaskBid', related_name='accepted_for_task', null=True, blank=True, on_delete=models.SET_NULL)
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
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content}"
    
    def content_snippet(self):
        return f"{self.content}"[:57] + "..."


class TaskBid(models.Model):
    freelancer = models.ForeignKey("accounts.Freelancer", on_delete=models.CASCADE)
    task = models.ForeignKey(Task, related_name='bids', on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    expected_delivery_time = models.IntegerField()
    expected_delivery_time_measurement = models.CharField(max_length=50)
    accepted = models.BooleanField(default=False)
    completed_on_time = models.BooleanField(default=False)  # New field
    completed_within_budget = models.BooleanField(default=False) 
    timestamp = models.DateTimeField(auto_now_add=True)


FREELANCER_NOTIFICATION_CAT = (
    ("review","review"),
    ("hired","hired"),
    ("due date","due date"),
    ("message","message"),
)
class FreelancerNotification(models.Model):
    freelancer = models.ForeignKey("accounts.Freelancer", on_delete=models.CASCADE)
    notification_category = models.CharField(max_length=50, choices=FREELANCER_NOTIFICATION_CAT)
    read = models.BooleanField(default=False)
    task = models.ForeignKey(Task, null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    message = models.ForeignKey(PrivateMessage, null=True, blank=True, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

# {% url 'home:single_task_view' ID=notification.task.id %}
EMPLOYER_NOTIFICATION_CAT = (
    ("review","review"),
    ("bid","bid"),
    ("task expiring","task expiring"),
    ("message","message"),
)
class EmployerNotification(models.Model):
    employer = models.ForeignKey("accounts.Employer", on_delete=models.CASCADE)
    notification_category = models.CharField(max_length=50, choices=EMPLOYER_NOTIFICATION_CAT)
    read = models.BooleanField(default=False)
    task = models.ForeignKey(Task, null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    message = models.ForeignKey(PrivateMessage, null=True, blank=True, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class FreelancerReview(models.Model):
    freelancer = models.ForeignKey("accounts.Freelancer", on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


class EmployerReview(models.Model):
    employer = models.ForeignKey("accounts.Employer", on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


class FreelancerNote(models.Model):
    freelancer = models.ForeignKey("accounts.Freelancer", on_delete=models.CASCADE)
    priority = models.CharField(max_length=20)
    note = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


class EmployerNote(models.Model):
    employer = models.ForeignKey("accounts.Employer", on_delete=models.CASCADE)
    priority = models.CharField(max_length=20)
    note = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


class TaskPayment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='payments')
    employer = models.ForeignKey("accounts.Employer", on_delete=models.CASCADE)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_id = models.CharField(max_length=7, blank=True, null=True,unique=True)
    release_payment = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Generate a unique order ID with the specified format
        if not self.order_id:
            self.order_id = "#" + str(uuid.uuid4())[:5].upper()  # Generate UUID and take the first 5 characters
        super().save(*args, **kwargs)