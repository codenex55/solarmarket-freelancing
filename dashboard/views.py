from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import (Task, TaskFile, TaskBid, PrivateChat, PrivateMessage, TaskReview, 
    FreelancerNotification, EmployerNotification, FreelancerNote,EmployerNote, TaskPayment
)
from django.http import JsonResponse
from django.contrib.auth.models import User
from accounts.models import Freelancer, Employer, UserAdditionalInformation
from django.contrib import messages
import requests
from django.db.models import Q
from django.db.models import Count, Avg
from django.utils import timezone
from django.utils.timezone import now
from django.conf import settings
from django.db.models import Sum, OuterRef, Subquery, DateTimeField, CharField

# Create your views here.

def count_unread_messages(user_email):
    try:
        user = User.objects.get(email=user_email)
        
        # Get all chats where the user is a participant
        chats = PrivateChat.objects.filter(user1=user) | PrivateChat.objects.filter(user2=user)
        
        # Count unread messages where the user is not the sender
        unread_count = PrivateMessage.objects.filter(chat__in=chats,read=False).exclude(sender=user).count()

        return unread_count
    
    except User.DoesNotExist:
        print(f"No user found with email: {user_email}")
        return 0
    
def read_messages(user_email):
    try:
        user = User.objects.get(email=user_email)
        
        # Get all chats where the user is a participant
        chats = PrivateChat.objects.filter(user1=user) | PrivateChat.objects.filter(user2=user)
        
        # Count unread messages where the user is not the sender
        unread_count = PrivateMessage.objects.filter(chat__in=chats, read=False).exclude(sender=user).count()
        
        return unread_count
    
    except User.DoesNotExist:
        print(f"No user found with email: {user_email}")
        return 0
    

# EMPLOYER DECORATOR
from django.http import HttpResponseRedirect
from django.urls import reverse

class EmployerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('accounts:login_view'))

        user_type = request.user.useradditionalinformation.user_type
        if user_type != 'employer':
            return HttpResponseRedirect(reverse('accounts:login_view'))

        return super().dispatch(request, *args, **kwargs)


# EMPLOYER DASHBOARD

class EmployerDashBoardHome(LoginRequiredMixin, EmployerRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        employer = Employer.objects.get(user_additional_info=request.user.useradditionalinformation)

        # Number of Task posted
        tasks_posted_count = Task.objects.filter(user=request.user).count()

        # freelnacers_hired
        freelancers_hired = Task.objects.filter(user=request.user, accepted_bid__isnull=False).count()

        # Reviews Received
        # reviews_received_count = EmployerReview.objects.filter(employer=employer).count()

        # All Notification
        all_notification = EmployerNotification.objects.filter(read=False).exclude(notification_category="message").order_by("-timestamp")

        # notification count
        notification_count = EmployerNotification.objects.filter(read=False).exclude(notification_category="message").order_by("-timestamp").count()

        # All Message Notification
        all_message_notification = EmployerNotification.objects.filter(read=False, notification_category="message").order_by("-timestamp")

        # message notification count
        message_notification_count = EmployerNotification.objects.filter(read=False, notification_category="message").order_by("-timestamp").count()

        # All Notes
        all_notes = EmployerNote.objects.all().order_by("-timestamp")

        # all payment
        all_payment = TaskPayment.objects.all().order_by("-timestamp")

        unread_messages_count  = count_unread_messages(request.user.email)

        context = {
            "unread_messages_count":unread_messages_count,
            'tasks_posted_count': tasks_posted_count,
            'freelancers_hired': freelancers_hired,
            # 'reviews_received_count': reviews_received_count,
            "all_notification":all_notification,
            "all_notes":all_notes,
            "notification_count":notification_count,
            "all_payment":all_payment,
            "all_message_notification":all_message_notification,
            "message_notification_count":message_notification_count,
        }
        return render(request, "dashboard/employer-dashboard-home.html", context)
    

    def post(self, request, *args, **kwargs):
        priority = request.POST.get("priority")
        note = request.POST.get("note")
        employer = Employer.objects.get(user_additional_info=request.user.useradditionalinformation)
        EmployerNote.objects.create(employer=employer, priority=priority, note=note)
        return redirect("dashboard:employer_dashboard_home_view")
    

class EmployerPostTask(LoginRequiredMixin, EmployerRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # All Notification
        all_notification = EmployerNotification.objects.filter(read=False).exclude(notification_category="message").order_by("-timestamp")

        # notification count
        notification_count = EmployerNotification.objects.filter(read=False).exclude(notification_category="message").order_by("-timestamp").count()

        # All Message Notification
        all_message_notification = EmployerNotification.objects.filter(read=False, notification_category="message").order_by("-timestamp")

        # message notification count
        message_notification_count = EmployerNotification.objects.filter(read=False, notification_category="message").order_by("-timestamp").count()

        all_states = requests.get("https://nga-states-lga.onrender.com/fetch").json()

        unread_messages_count  = count_unread_messages(request.user.email)

        context = {
            "unread_messages_count":unread_messages_count,
            "all_states":all_states,
            "all_notification":all_notification,
            "notification_count":notification_count,
            "all_message_notification":all_message_notification,
            "message_notification_count":message_notification_count,
        }
        return render(request, "dashboard/employer-post-task.html", context)
    
    def post(self, request, *args, **kwargs):
        # Process form submission
        task_name = request.POST.get('task_name')
        task_category = request.POST.get('task_category')
        task_state = request.POST.get('state')
        task_lga = request.POST.get('lga')
        task_min_pay = request.POST.get('task_min_pay')
        task_max_pay = request.POST.get('task_max_pay')
        task_type = request.POST.get('task_type')
        task_deadline = request.POST.get('task_deadline')
        task_description = request.POST.get('task_description')
        task_files = request.FILES.getlist('task_files')

        # Save form data to the database
        task = Task(
            user = request.user,
            task_name=task_name,
            task_category=task_category,
            task_state=task_state,
            task_lga=task_lga,
            task_min_pay=task_min_pay,
            task_max_pay=task_max_pay,
            task_type=task_type,
            task_deadline=task_deadline,
            task_description=task_description
        )
        task.save()

        # Save task images
        for file in task_files:
            TaskFile.objects.create(task=task, file=file)

        return redirect("dashboard:employer_manage_task_view")
    

class DeleteTaskView(LoginRequiredMixin, EmployerRequiredMixin, View):
    def get(self, request, TASK_ID, *args, **kwargs):
        Task.objects.get(id=TASK_ID).delete()
        return redirect("dashboard:employer_manage_task_view")
    

class EmployerManageTask(LoginRequiredMixin, EmployerRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # All Notification
        all_notification = EmployerNotification.objects.filter(read=False).exclude(notification_category="message").order_by("-timestamp")

        # notification count
        notification_count = EmployerNotification.objects.filter(read=False).exclude(notification_category="message").order_by("-timestamp").count()

        # All Message Notification
        all_message_notification = EmployerNotification.objects.filter(read=False, notification_category="message").order_by("-timestamp")

        # message notification count
        message_notification_count = EmployerNotification.objects.filter(read=False, notification_category="message").order_by("-timestamp").count()

        unread_messages_count  = count_unread_messages(request.user.email)

        tasks  = Task.objects.filter(user=request.user).order_by("-timestamp")

        tasks_with_bids_info = []

        for task in tasks:
            remaining_time = task.task_deadline - timezone.now()

            # Retrieve TaskBid objects related to the current task
            task_bids = TaskBid.objects.filter(task=task)

            # Count how many TaskBid objects (bids) are related to the current task
            bids_count = task_bids.count()

            # Calculate the average bidding price for the current task
            average_bid_price = task_bids.aggregate(Avg('bid_amount'))['bid_amount__avg']

            if remaining_time.days > 0:
                remaining_time = f"{remaining_time.days} days, {remaining_time.seconds // 3600} hours left"
            elif remaining_time.seconds >= 3600:
                remaining_time = f"{remaining_time.seconds // 3600} hours left"
            elif remaining_time.seconds > 0:
                remaining_time = f"{remaining_time.seconds // 60} minutes left"
            else:
                remaining_time = "Expired"

            # Append task with bids info to the list
            tasks_with_bids_info.append({
                'task': task,
                "remaining_time":remaining_time,
                'bids_count': bids_count,
                'average_bid_price': average_bid_price or 0,  # Handle case when there are no bids
                "all_notification":all_notification,
                "notification_count":notification_count,
                "all_message_notification":all_message_notification,
                "message_notification_count":message_notification_count,
                "unread_messages_count":unread_messages_count,
            })

        # Pass the tasks with bids info to the template
        context = {'all_task': tasks_with_bids_info}
        return render(request, "dashboard/employer-manage-task.html", context)
    

class EmployerManageBidder(LoginRequiredMixin, EmployerRequiredMixin, View):
    def get(self, request, TASK_ID, *args, **kwargs):
        # All Notification
        all_notification = EmployerNotification.objects.filter(read=False).exclude(notification_category="message").order_by("-timestamp")

        # notification count
        notification_count = EmployerNotification.objects.filter(read=False).exclude(notification_category="message").order_by("-timestamp").count()

        # All Message Notification
        all_message_notification = EmployerNotification.objects.filter(read=False, notification_category="message").order_by("-timestamp")

        # message notification count
        message_notification_count = EmployerNotification.objects.filter(read=False, notification_category="message").order_by("-timestamp").count()

        task = Task.objects.get(id=TASK_ID)

        # Retrieve all bidders for the task
        bidders = TaskBid.objects.filter(task=task)
        count = bidders.count()

        paystack_public_key = settings.PAYSTACK_PUBLIC_KEY

        unread_messages_count  = count_unread_messages(request.user.email)

        context = {
            "unread_messages_count":unread_messages_count,
            'task': task,
            'bidders': bidders,
            "count":count,
            "paystack_public_key":paystack_public_key,
            "all_notification":all_notification,
            "notification_count":notification_count,
            "all_message_notification":all_message_notification,
            "message_notification_count":message_notification_count,
        }

        return render(request, "dashboard/employer-manage-bidders.html", context)
    

class EmployerRemoveBidder(LoginRequiredMixin, EmployerRequiredMixin, View):
    def get(self, request, BID_ID, *args, **kwargs):
        bid = TaskBid.objects.get(id=BID_ID)
        task_id = bid.task.id
        bid.delete()
        return redirect("dashboard:employer_manage_bidder_view", TASK_ID=task_id)
    

class EmployerBookmark(LoginRequiredMixin, EmployerRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        employer = Employer.objects.get(user_additional_info=request.user.useradditionalinformation)
        bookmarked_freelancers = employer.bookmark_freelancer.all()
        bookmarked_tasks = employer.bookmark_task.all()
        
        unread_messages_count  = count_unread_messages(request.user.email)

        # All Notification
        all_notification = EmployerNotification.objects.filter(read=False).exclude(notification_category="message").order_by("-timestamp")

        # notification count
        notification_count = EmployerNotification.objects.filter(read=False).exclude(notification_category="message").order_by("-timestamp").count()

        # All Message Notification
        all_message_notification = EmployerNotification.objects.filter(read=False, notification_category="message").order_by("-timestamp")

        # message notification count
        message_notification_count = EmployerNotification.objects.filter(read=False, notification_category="message").order_by("-timestamp").count()

        context = {
            "unread_messages_count":unread_messages_count,
            "bookmarked_freelancers":bookmarked_freelancers,
            "bookmarked_tasks":bookmarked_tasks,
            "all_notification":all_notification,
            "notification_count":notification_count,
            "all_message_notification":all_message_notification,
            "message_notification_count":message_notification_count,
        }
        return render(request, "dashboard/employer-bookmark.html", context)
    
    def post(self, request, *args, **kwargs):
        # to remove bookmarked freelancer
        return JsonResponse({"message":"success"})
    

class EmployerReviewView(LoginRequiredMixin, EmployerRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        employer = Employer.objects.get(user_additional_info=request.user.useradditionalinformation)

        # All Notification
        all_notification = EmployerNotification.objects.filter(read=False).exclude(notification_category="message").order_by("-timestamp")

        # notification count
        notification_count = EmployerNotification.objects.filter(read=False).exclude(notification_category="message").order_by("-timestamp").count()

        # All Message Notification
        all_message_notification = EmployerNotification.objects.filter(read=False, notification_category="message").order_by("-timestamp")

        # message notification count
        message_notification_count = EmployerNotification.objects.filter(read=False, notification_category="message").order_by("-timestamp").count()

        task_review = TaskReview.objects.all().order_by("-timestamp")

        unread_messages_count  = count_unread_messages(request.user.email)

        context = {
            "unread_messages_count":unread_messages_count,
            "all_notification":all_notification,
            "notification_count":notification_count,
            "all_message_notification":all_message_notification,
            "message_notification_count":message_notification_count,
            "task_review":task_review
        }
        return render(request, "dashboard/employer-review.html",  context)
    
    def post(self, request, *args, **kwargs):
        # to add review and edit it
        return JsonResponse({"message":"success"})
    
    
class EmployerSettings(LoginRequiredMixin, EmployerRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # All Notification
        all_notification = EmployerNotification.objects.filter(read=False).exclude(notification_category="message").order_by("-timestamp")

        # notification count
        notification_count = EmployerNotification.objects.filter(read=False).exclude(notification_category="message").order_by("-timestamp").count()

        # All Message Notification
        all_message_notification = EmployerNotification.objects.filter(read=False, notification_category="message").order_by("-timestamp")

        # message notification count
        message_notification_count = EmployerNotification.objects.filter(read=False, notification_category="message").order_by("-timestamp").count()

        unread_messages_count  = count_unread_messages(request.user.email)

        context = {
            "unread_messages_count":unread_messages_count,
            "all_notification":all_notification,
            "notification_count":notification_count,
            "all_message_notification":all_message_notification,
            "message_notification_count":message_notification_count,
        }
        return render(request, "dashboard/employer-settings.html", context)
    
    def post(self, request, *args, **kwargs):
        # to save changes
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        current_password = request.POST.get('current_password')

        current_user = request.user.username
        user = User.objects.get(username=current_user)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        if current_password:
            new_password = request.POST.get('new_password')
            confirm_new_password = request.POST.get('confirm_new_password')
        
        messages.success(request, "Accounts information updated successfully!")
        return redirect("dashboard:employer_settings_view")
    

class EmployerPaymentSuccess(LoginRequiredMixin, EmployerRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # All Notification
        all_notification = EmployerNotification.objects.filter(read=False).exclude(notification_category="message").order_by("-timestamp")

        # notification count
        notification_count = EmployerNotification.objects.filter(read=False).exclude(notification_category="message").order_by("-timestamp").count()

        # All Message Notification
        all_message_notification = EmployerNotification.objects.filter(read=False, notification_category="message").order_by("-timestamp")

        # message notification count
        message_notification_count = EmployerNotification.objects.filter(read=False, notification_category="message").order_by("-timestamp").count()

        unread_messages_count  = count_unread_messages(request.user.email)

        context = {
            "unread_messages_count":unread_messages_count,
            "all_notification":all_notification,
            "notification_count":notification_count,
            "all_message_notification":all_message_notification,
            "message_notification_count":message_notification_count,
        }
        return render(request, "dashboard/employer-payment-success.html", context)






# FREELANCER DECORATOR
class FreelancerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('accounts:login_view'))

        user_type = request.user.useradditionalinformation.user_type
        if user_type != 'freelancer':
            return HttpResponseRedirect(reverse('accounts:login_view'))

        return super().dispatch(request, *args, **kwargs)


# FREELANCER DASHBOARD

class FreelancerDashBoardHome(LoginRequiredMixin, FreelancerRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        freelancer = Freelancer.objects.get(user_additional_info=request.user.useradditionalinformation)

        # Number of Task Bids Won
        tasks_won_count = TaskBid.objects.filter(freelancer=freelancer, accepted=True).count()

        # Amount Made
        amount_made = TaskBid.objects.filter(freelancer=freelancer, task__accepted_bid__freelancer=freelancer).aggregate(total_amount=Sum('bid_amount'))['total_amount'] or 0

        # Reviews Received
        # reviews_received_count = FreelancerReview.objects.filter(freelancer=freelancer).count()

        # All Notification
        all_notification = FreelancerNotification.objects.filter(read=False).exclude(notification_category="message").order_by("-timestamp")

        # notification count
        notification_count = FreelancerNotification.objects.filter(read=False).exclude(notification_category="message").order_by("-timestamp").count()

        # All Notes
        all_notes = FreelancerNote.objects.all().order_by("-timestamp")

        # Bid Count
        freelancer = Freelancer.objects.get(user_additional_info=request.user.useradditionalinformation)
        bid_count = TaskBid.objects.filter(freelancer=freelancer).count()

        # Task Payment
        task_payments = TaskPayment.objects.filter(task__bids__freelancer=freelancer)

        # All Message Notification
        all_message_notification = FreelancerNotification.objects.filter(read=False, notification_category="message").order_by("-timestamp")

        # message notification count
        message_notification_count = FreelancerNotification.objects.filter(read=False, notification_category="message").order_by("-timestamp").count()

        unread_messages_count  = count_unread_messages(request.user.email)

        context = {
            "unread_messages_count":unread_messages_count,
            'tasks_won_count': tasks_won_count,
            'amount_made': amount_made,
            # 'reviews_received_count': reviews_received_count,
            "all_notification":all_notification,
            "all_notes":all_notes,
            "notification_count":notification_count,
            "bid_count":bid_count,
            "task_payments":task_payments,
            "all_message_notification":all_message_notification,
            "message_notification_count":message_notification_count,
        }
        return render(request, "dashboard/freelancer-dashboard-home.html", context)
    
    def post(self, request, *args, **kwargs):
        priority = request.POST.get("priority")
        note = request.POST.get("note")
        freelancer = Freelancer.objects.get(user_additional_info=request.user.useradditionalinformation)
        FreelancerNote.objects.create(freelancer=freelancer, priority=priority, note=note)
        return redirect("dashboard:freelancer_dashboard_home_view")

    

class FreelancerBookmark(LoginRequiredMixin, FreelancerRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # All Notification
        all_notification = FreelancerNotification.objects.filter(read=False).exclude(notification_category="message").order_by("-timestamp")

        # notification count
        notification_count = FreelancerNotification.objects.filter(read=False).exclude(notification_category="message").order_by("-timestamp").count()

        # All Message Notification
        all_message_notification = FreelancerNotification.objects.filter(read=False, notification_category="message").order_by("-timestamp")

        # message notification count
        message_notification_count = FreelancerNotification.objects.filter(read=False, notification_category="message").order_by("-timestamp").count()

        # Bid Count
        freelancer = Freelancer.objects.get(user_additional_info=request.user.useradditionalinformation)
        bid_count = TaskBid.objects.filter(freelancer=freelancer).count()

        bookmarked_freelancers = freelancer.bookmark_freelancer.all()
        bookmarked_tasks = freelancer.bookmark_task.all()
        unread_messages_count  = count_unread_messages(request.user.email)

        context = {
            "unread_messages_count":unread_messages_count,
            "all_notification":all_notification,
            "notification_count":notification_count,
            "bid_count":bid_count,
            "all_message_notification":all_message_notification,
            "message_notification_count":message_notification_count,
            "bookmarked_freelancers":bookmarked_freelancers,
            "bookmarked_tasks":bookmarked_tasks

        }
        return render(request, "dashboard/freelancer-bookmark.html", context)
    
    def post(self, request, *args, **kwargs):
        # to remove bookmarked task
        return JsonResponse({"message":"success"})
    

class FreelancerActiveBids(LoginRequiredMixin, FreelancerRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        freelancer = Freelancer.objects.get(user_additional_info=request.user.useradditionalinformation)
        bids = TaskBid.objects.filter(freelancer=freelancer)

        # Bid Count
        bid_count = TaskBid.objects.filter(freelancer=freelancer).count()

        # All Notification
        all_notification = FreelancerNotification.objects.filter(read=False).exclude(notification_category="message").order_by("-timestamp")

        # notification count
        notification_count = FreelancerNotification.objects.filter(read=False).exclude(notification_category="message").order_by("-timestamp").count()

        # All Message Notification
        all_message_notification = FreelancerNotification.objects.filter(read=False, notification_category="message").order_by("-timestamp")

        # message notification count
        message_notification_count = FreelancerNotification.objects.filter(read=False, notification_category="message").order_by("-timestamp").count()

        unread_messages_count  = count_unread_messages(request.user.email)

        context = {
            "unread_messages_count":unread_messages_count,
            "bids":bids,
            "bid_count":bid_count,
            "all_notification":all_notification,
            "notification_count":notification_count,
            "all_message_notification":all_message_notification,
            "message_notification_count":message_notification_count,
        }
        return render(request, "dashboard/freelancer-active-bids.html", context)
    

class FreelancerReviewView(LoginRequiredMixin, FreelancerRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # All Notification
        all_notification = FreelancerNotification.objects.filter(read=False).exclude(notification_category="message").order_by("-timestamp")

        # notification count
        notification_count = FreelancerNotification.objects.filter(read=False).exclude(notification_category="message").order_by("-timestamp").count()

        # All Message Notification
        all_message_notification = FreelancerNotification.objects.filter(read=False, notification_category="message").order_by("-timestamp")

        # message notification count
        message_notification_count = FreelancerNotification.objects.filter(read=False, notification_category="message").order_by("-timestamp").count()

        # Bid Count
        freelancer = Freelancer.objects.get(user_additional_info=request.user.useradditionalinformation)
        bid_count = TaskBid.objects.filter(freelancer=freelancer).count()

        # all_review = FreelancerReview.objects.filter(freelancer=freelancer).order_by("-timestamp")

        unread_messages_count  = count_unread_messages(request.user.email)

        context = {
            "unread_messages_count":unread_messages_count,
            "all_notification":all_notification,
            "notification_count":notification_count,
            "bid_count":bid_count,
            "all_message_notification":all_message_notification,
            "message_notification_count":message_notification_count,
            # "all_review":all_review
        }
        return render(request, "dashboard/freelancer-review.html", context)
    
    def post(self, request, *args, **kwargs):
        # to add review and edit it
        return JsonResponse({"message":"success"})
    

class DeleteBidView(LoginRequiredMixin, FreelancerRequiredMixin, View):
    def get(self, request, BID_ID, *args, **kwargs):
        TaskBid.objects.get(id=BID_ID).delete()
        return redirect("dashboard:freelancer_active_bids_view")
    
    
class FreelancerSettings(LoginRequiredMixin, FreelancerRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        all_states = requests.get("https://nga-states-lga.onrender.com/fetch").json()
        freelancer = Freelancer.objects.get(user_additional_info=request.user.useradditionalinformation)

        # All Notification
        all_notification = FreelancerNotification.objects.filter(read=False).exclude(notification_category="message").order_by("-timestamp")

        # notification count
        notification_count = FreelancerNotification.objects.filter(read=False).exclude(notification_category="message").order_by("-timestamp").count()

        # All Message Notification
        all_message_notification = FreelancerNotification.objects.filter(read=False, notification_category="message").order_by("-timestamp")

        # message notification count
        message_notification_count = FreelancerNotification.objects.filter(read=False, notification_category="message").order_by("-timestamp").count()

        # Bid Count
        freelancer = Freelancer.objects.get(user_additional_info=request.user.useradditionalinformation)
        bid_count = TaskBid.objects.filter(freelancer=freelancer).count()

        unread_messages_count  = count_unread_messages(request.user.email)

        context = {
            "unread_messages_count":unread_messages_count,
            "all_states":all_states,
            "freelancer":freelancer,
            "all_notification":all_notification,
            "notification_count":notification_count,
            "bid_count":bid_count,
            "all_message_notification":all_message_notification,
            "message_notification_count":message_notification_count,
        }
        if freelancer.state:
            all_lgas = requests.get(f"https://nga-states-lga.onrender.com/?state={freelancer.state}").json()
            context["all_lgas"] = all_lgas

        return render(request, "dashboard/freelancer-settings.html", context)
    
    def post(self, request, *args, **kwargs):
        # to save changes
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        state = request.POST.get('state')
        lga = request.POST.get('lga')
        tagline = request.POST.get('tagline')
        speciality = request.POST.get('speciality')
        description = request.POST.get('description')
        minimum_pay = float(request.POST.get("minimum_pay"))
        current_password = request.POST.get('current_password')
        profile_picture = request.FILES.get("profile_picture")

        current_user = request.user.username
        user = User.objects.get(username=current_user)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        if profile_picture:
            user_info = UserAdditionalInformation.objects.get(user=request.user)
            user_info.profile_picture = profile_picture
            user_info.save()

        freelancer = Freelancer.objects.get(user_additional_info=request.user.useradditionalinformation)
        freelancer.state = state
        freelancer.lga = lga
        freelancer.tagline = tagline
        freelancer.self_introduction = description
        freelancer.speciality = speciality
        freelancer.minimum_pay = minimum_pay
        freelancer.save()

        if current_password:
            new_password = request.POST.get('new_password')
            confirm_new_password = request.POST.get('confirm_new_password')
        
        messages.success(request, "Accounts information updated successfully!")
        return redirect("dashboard:freelancer_settings_view")
    


# CHAT SYSTEM

class FreelancerMessages(LoginRequiredMixin, View):
    def get(self, request, CHAT_ID, *args, **kwargs):
        # FreelancerNotification.objects.all().delete()
        # EmployerNotification.objects.all().delete()
        # PrivateChat.objects.all().delete()
        # PrivateMessage.objects.all().delete()
        # All Notification
        all_notification = FreelancerNotification.objects.filter(read=False).exclude(notification_category="message").order_by("-timestamp")

        # notification count
        notification_count = FreelancerNotification.objects.filter(read=False).exclude(notification_category="message").order_by("-timestamp").count()

        # All Message Notification
        all_message_notification = FreelancerNotification.objects.filter(read=False, notification_category="message").order_by("-timestamp")

        # message notification count
        message_notification_count = FreelancerNotification.objects.filter(read=False, notification_category="message").order_by("-timestamp").count()

        # Bid Count
        freelancer = Freelancer.objects.get(user_additional_info=request.user.useradditionalinformation)
        bid_count = TaskBid.objects.filter(freelancer=freelancer).count()

        # Subquery to get the last message content and timestamp for each chat
        last_message_subquery = PrivateMessage.objects.filter(
            chat=OuterRef('pk')
        ).order_by('-timestamp').values('content', 'timestamp')[:1]

        # Annotate each chat with its latest message content and timestamp
        all_chats = PrivateChat.objects.filter(
            Q(user1=request.user) | Q(user2=request.user)
        ).annotate(
            last_message_content=Subquery(last_message_subquery.values('content')[:1], output_field=CharField()),
            last_message_timestamp=Subquery(last_message_subquery.values('timestamp')[:1], output_field=DateTimeField())
        ).order_by('-last_message_timestamp')

        # Count unread messages
        unread_messages_count  = count_unread_messages(request.user.email)

        if CHAT_ID == 0:
            context = {
                "unread_messages_count":unread_messages_count,
                "all_chats":all_chats,
                "chat_id":CHAT_ID,
                "all_notification":all_notification,
                "notification_count":notification_count,
                "bid_count":bid_count,
                "all_message_notification":all_message_notification,
                "message_notification_count":message_notification_count,
            }
            return render(request, 'dashboard/freelancer-messages.html', context)
        else:
            chat = PrivateChat.objects.get(id=CHAT_ID)

            # Ensure the current user is a participant in the chat
            if request.user not in [chat.user1, chat.user2]:
                 return redirect('dashboard:freelancer_messages_view', CHAT_ID=0)
            
            messages = PrivateMessage.objects.filter(chat=chat).order_by('timestamp')

            # Filter messages where the request.user is not the sender and the message is not already read
            unread_messages = PrivateMessage.objects.filter(
                Q(chat__user1=request.user) | Q(chat__user2=request.user),
                ~Q(sender=request.user),
                read=False
            )
            # Mark these messages as read
            unread_messages.update(read=True)

            free_not = FreelancerNotification.objects.filter(freelancer=freelancer, notification_category="message")
            free_not.update(read=True)

            # Group messages by date
            messages_by_day = {}
            today = timezone.now().date()

            for message in messages:
                timestamp = message.timestamp
                msg_date = timestamp.date()

                if msg_date not in messages_by_day:
                    messages_by_day[msg_date] = []
                messages_by_day[msg_date].append(message)

            if request.user == chat.user1:
                chat_recipient = chat.user2
            else:
                chat_recipient = chat.user1

            context = {
                'messages_by_day': messages_by_day,
                'unread_messages_count': unread_messages_count,
                "today": today,
                "chat_id":CHAT_ID,
                "all_chats":all_chats,
                'messages': messages,
                "chat_recipient":chat_recipient,
                "all_notification":all_notification,
                "notification_count":notification_count,
                "bid_count":bid_count,
                "all_message_notification":all_message_notification,
                "message_notification_count":message_notification_count,
            }
            return render(request, 'dashboard/freelancer-messages.html', context)
    

class EmployerMessages(LoginRequiredMixin, View):
    def get(self, request, CHAT_ID, *args, **kwargs):
        # All Notification
        all_notification = EmployerNotification.objects.filter(read=False).exclude(notification_category="message").order_by("-timestamp")

        # notification count
        notification_count = EmployerNotification.objects.filter(read=False).exclude(notification_category="message").order_by("-timestamp").count()

        # All Message Notification
        all_message_notification = EmployerNotification.objects.filter(read=False, notification_category="message").order_by("-timestamp")

        # message notification count
        message_notification_count = EmployerNotification.objects.filter(read=False, notification_category="message").order_by("-timestamp").count()

        employer = Employer.objects.get(user_additional_info=request.user.useradditionalinformation)

        # Subquery to get the last message content and timestamp for each chat
        last_message_subquery = PrivateMessage.objects.filter(
            chat=OuterRef('pk')
        ).order_by('-timestamp').values('content', 'timestamp')[:1]

        # Annotate each chat with its latest message content and timestamp
        all_chats = PrivateChat.objects.filter(
            Q(user1=request.user) | Q(user2=request.user)
        ).annotate(
            last_message_content=Subquery(last_message_subquery.values('content')[:1], output_field=CharField()),
            last_message_timestamp=Subquery(last_message_subquery.values('timestamp')[:1], output_field=DateTimeField())
        ).order_by('-last_message_timestamp')

        unread_messages_count  = count_unread_messages(request.user.email)

        if CHAT_ID == 0:
            context = {
                "unread_messages_count":unread_messages_count,
                "all_chats":all_chats,
                "chat_id":CHAT_ID,
                "all_notification":all_notification,
                "notification_count":notification_count,
                "all_message_notification":all_message_notification,
                "message_notification_count":message_notification_count,
            }
            return render(request, 'dashboard/employer-messages.html', context)
        else:
            chat = PrivateChat.objects.get(id=CHAT_ID)

            # Ensure the current user is a participant in the chat
            if request.user not in [chat.user1, chat.user2]:
                 return redirect('dashboard:employer_messages_view', CHAT_ID=0)
            
            messages = PrivateMessage.objects.filter(chat=chat).order_by('timestamp')

            # Filter messages where the request.user is not the sender and the message is not already read
            unread_messages = PrivateMessage.objects.filter(
                Q(chat__user1=request.user) | Q(chat__user2=request.user),
                ~Q(sender=request.user),
                read=False
            )

            # Mark these messages as read
            unread_messages.update(read=True)

            emp_not = EmployerNotification.objects.filter(employer=employer, notification_category="message")
            emp_not.update(read=True)

            # Group messages by date
            messages_by_day = {}
            today = timezone.now().date()

            for message in messages:
                timestamp = message.timestamp
                msg_date = timestamp.date()

                if msg_date not in messages_by_day:
                    messages_by_day[msg_date] = []
                messages_by_day[msg_date].append(message)

            if request.user == chat.user1:
                chat_recipient = chat.user2
            else:
                chat_recipient = chat.user1

            context = {
                'messages_by_day': messages_by_day,
                'unread_messages_count': unread_messages_count,
                "today": today,
                "chat_id":CHAT_ID,
                "all_chats":all_chats,
                'messages': messages,
                "chat_recipient":chat_recipient,
                "all_notification":all_notification,
                "notification_count":notification_count,
                "all_message_notification":all_message_notification,
                "message_notification_count":message_notification_count,
            }
            return render(request, 'dashboard/employer-messages.html', context)


class InitiateChatView(LoginRequiredMixin, View):
    def get(self, request, RECIPIENT_ID, *args, **kwargs):
        recipient = User.objects.get(id=RECIPIENT_ID)

        # Check if a chat already exists between the current user and the recipient
        existing_chat = PrivateChat.objects.filter(user1=request.user, user2=recipient)
        if existing_chat.exists():
            print("here")
            chat = existing_chat.first()
        else:
            # Create a new chat if one doesn't exist
            print("here now")
            chat = PrivateChat.objects.create(user1=request.user, user2=recipient)

        if UserAdditionalInformation.objects.get(user=request.user).user_type == "freelancer":
            return redirect('dashboard:freelancer_messages_view', CHAT_ID=chat.id)
        else:
            return redirect('dashboard:employer_messages_view', CHAT_ID=chat.id)


class SendMessage(LoginRequiredMixin, View):
    def post(self, request, CHAT_ID, *args, **kwargs):
        print(CHAT_ID)
        chat = PrivateChat.objects.get(id=CHAT_ID)

        # Ensure the current user is a participant in the chat
        if request.user not in [chat.user1, chat.user2]:
            if request.user.useradditionalinformation.user_type == "freelancer":
                return redirect('dashboard:freelancer_messages_view', CHAT_ID=0)
            else:
                return redirect('dashboard:employer_messages_view', CHAT_ID=0)
            
        # create notification
         
        
        content = request.POST.get('content')
        sender = request.user

        message = PrivateMessage.objects.create(chat=chat, sender=sender, content=content)

        # Identify the recipient
        recipient = chat.user2 if chat.user1 == request.user else chat.user1

        # Create notification for the recipient
        if recipient.useradditionalinformation.user_type == "freelancer":
            freelancer_profile = Freelancer.objects.get(user_additional_info__user=recipient)
            FreelancerNotification.objects.create(
                freelancer=freelancer_profile,
                notification_category="message",
                user=sender,
                message = message
            )
        elif recipient.useradditionalinformation.user_type == "employer":
            employer_profile = Employer.objects.get(user_additional_info__user=recipient)
            EmployerNotification.objects.create(
                employer=employer_profile,
                notification_category="message",
                user=sender,
                message = message
            )

        if request.user.useradditionalinformation.user_type == "freelancer":
            return redirect('dashboard:freelancer_messages_view', CHAT_ID=CHAT_ID)
        else:
            return redirect('dashboard:employer_messages_view', CHAT_ID=CHAT_ID)



# PAYMENT VERIFICATION

class VerifyPaymentView(View):
    def post(self, request, *args, **kwargs):
        ref = request.POST.get("ref")
        bidder_id = int(request.POST.get("bidder_id"))
        task_id = int(request.POST.get("task_id"))

        url = f"https://api.paystack.co/transaction/verify/{ref}"
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.get(url, headers=headers)
        response_data = response.json()

        if response_data['status']:
            transaction_data = response_data['data']
            if transaction_data['status'] == 'success':
                # Do something with the transaction data
                task = Task.objects.get(id=task_id)
                employer = Employer.objects.get(user_additional_info=request.user.useradditionalinformation)
                task_bid = TaskBid.objects.get(id=bidder_id)

                TaskPayment.objects.create(employer=employer, task=task, payment_amount=task_bid.bid_amount)
                FreelancerNotification.objects.create(freelancer=task_bid.freelancer, notification_category="hired", task=task)
                TaskReview.objects.create(employer=employer, task=task)

                task_bid.accepted = True
                task_bid.save()
                if task.accepted_bid != None:
                    task.accepted_bid = task_bid
                    task.save()
                return JsonResponse({'status': 'success', 'message': 'Transaction verified'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Transaction failed'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Verification failed'})
        

