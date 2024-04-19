from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task
from django.http import JsonResponse
from django.contrib.auth.models import User
from accounts.models import Freelancer, Employer, UserAdditionalInformation
from django.contrib import messages
import requests
from .models import PrivateChat, PrivateMessage
from django.db.models import Q

# Create your views here.

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
        return render(request, "dashboard/employer-dashboard-home.html")
    

class EmployerPostTask(LoginRequiredMixin, EmployerRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {
        }
        return render(request, "dashboard/employer-post-task.html", context)
    
    def post(self, request, *args, **kwargs):
        # Process form submission
        task_name = request.POST.get('task_name')
        task_category = request.POST.get('task_category')
        task_location = request.POST.get('task_location')
        task_min_pay = request.POST.get('task_min_pay')
        task_max_pay = request.POST.get('task_max_pay')
        task_type = request.POST.get('task_type')
        task_skills = request.POST.get('task_skills')
        task_deadline = request.POST.get('task_deadline')
        task_description = request.POST.get('task_description')
        task_images = request.FILES.getlist('task_images')

        print(request.user)

        # Save form data to the database
        # task = Task(
        #     user = request.user,
        #     task_name=task_name,
        #     task_category=task_category,
        #     task_location=task_location,
        #     task_min_pay=task_min_pay,
        #     task_max_pay=task_max_pay,
        #     task_type=task_type,
        #     task_skills=task_skills,
        #     task_deadline=task_deadline,
        #     task_description=task_description
        # )
        # task.save()

        # Save task images
        # for image in task_images:
        #     task.task_images.create(image=image)

        return redirect("dashboard:employer_manage_task_view")
    

class EmployerManageTask(LoginRequiredMixin, EmployerRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        all_task = Task.objects.filter(user=request.user).order_by("-timestamp")
        context = {
            "all_task":all_task
        }
        return render(request, "dashboard/employer-manage-task.html", context)
    

class EmployerBookmark(LoginRequiredMixin, EmployerRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, "dashboard/employer-bookmark.html")
    
    def post(self, request, *args, **kwargs):
        # to remove bookmarked freelancer
        return JsonResponse({"message":"success"})
    

class EmployerReview(LoginRequiredMixin, EmployerRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, "dashboard/employer-review.html")
    
    def post(self, request, *args, **kwargs):
        # to add review and edit it
        return JsonResponse({"message":"success"})
    
    
class EmployerSettings(LoginRequiredMixin, EmployerRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, "dashboard/employer-settings.html")
    
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
        return render(request, "dashboard/freelancer-dashboard-home.html")
    

class FreelancerBookmark(LoginRequiredMixin, FreelancerRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, "dashboard/freelancer-bookmark.html")
    
    def post(self, request, *args, **kwargs):
        # to remove bookmarked task
        return JsonResponse({"message":"success"})
    

class FreelancerReview(LoginRequiredMixin, FreelancerRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, "dashboard/freelancer-review.html")
    
    def post(self, request, *args, **kwargs):
        # to add review and edit it
        return JsonResponse({"message":"success"})
    
    
class FreelancerSettings(LoginRequiredMixin, FreelancerRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        all_states = requests.get("https://nga-states-lga.onrender.com/fetch").json()
        freelancer = Freelancer.objects.get(user_additional_info=request.user.useradditionalinformation)
        context = {
            "all_states":all_states,
            "freelancer":freelancer
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
        all_chats = PrivateChat.objects.filter(Q(user1=request.user) | Q(user2=request.user))

        if CHAT_ID == 0:
            context = {
                "all_chats":all_chats,
                "chat_id":CHAT_ID
            }
            return render(request, 'dashboard/freelancer-messages.html', context)
        else:
            chat = PrivateChat.objects.get(id=CHAT_ID)

            # Ensure the current user is a participant in the chat
            if request.user not in [chat.user1, chat.user2]:
                 return redirect('dashboard:freelancer_messages_view', CHAT_ID=0)
            
            messages = PrivateMessage.objects.filter(chat=chat).order_by('timestamp')

            if request.user == chat.user1:
                chat_recipient = chat.user2
            else:
                chat_recipient = chat.user1

            context = {
                "chat_id":CHAT_ID,
                "all_chats":all_chats,
                'messages': messages,
                "chat_recipient":chat_recipient
            }
            return render(request, 'dashboard/freelancer-messages.html', context)
    

class EmployerMessages(LoginRequiredMixin, View):
    def get(self, request, CHAT_ID, *args, **kwargs):
        all_chats = PrivateChat.objects.filter(Q(user1=request.user) | Q(user2=request.user))
        if CHAT_ID == 0:
            context = {
                "all_chats":all_chats,
                "chat_id":CHAT_ID
            }
            return render(request, 'dashboard/employer-messages.html', context)
        else:
            chat = PrivateChat.objects.get(id=CHAT_ID)

            # Ensure the current user is a participant in the chat
            if request.user not in [chat.user1, chat.user2]:
                 return redirect('dashboard:employer_messages_view', CHAT_ID=0)
            
            messages = PrivateMessage.objects.filter(chat=chat).order_by('timestamp')

            if request.user == chat.user1:
                chat_recipient = chat.user2
            else:
                chat_recipient = chat.user1

            context = {
                "chat_id":CHAT_ID,
                "all_chats":all_chats,
                'messages': messages,
                "chat_recipient":chat_recipient
            }
            return render(request, 'dashboard/employer-messages.html', context)


class InitiateChatView(LoginRequiredMixin, View):
    def get(self, request, RECIPIENT_ID, *args, **kwargs):
        recipient = User.objects.get(id=RECIPIENT_ID)

        # Check if a chat already exists between the current user and the recipient
        existing_chat = PrivateChat.objects.filter(user1=request.user, user2=recipient)
        if existing_chat.exists():
            chat = existing_chat.first()
        else:
            # Create a new chat if one doesn't exist
            chat = PrivateChat.objects.create(user1=request.user, user2=recipient)

        if UserAdditionalInformation.objects.get(user=request.user).user_type == "freelancer":
            return redirect('dashboard:freelancer_messages_view', CHAT_ID=chat.id)
        else:
            return redirect('dashboard:employer_messages_view', CHAT_ID=chat.id)


class SendMessage(LoginRequiredMixin, View):
    def post(self, request, CHAT_ID, *args, **kwargs):
        chat = PrivateChat.objects.get(id=CHAT_ID)

        # Ensure the current user is a participant in the chat
        if request.user not in [chat.user1, chat.user2]:
            if request.user.useradditionalinformation.user_type == "freelancer":
                return redirect('dashboard:freelancer_messages_view', CHAT_ID=0)
            else:
                return redirect('dashboard:employer_messages_view', CHAT_ID=0)
        
        content = request.POST.get('content')
        sender = request.user
        print(sender.first_name)
        PrivateMessage.objects.create(chat=chat, sender=sender, content=content)

        if request.user.useradditionalinformation.user_type == "freelancer":
            return redirect('dashboard:freelancer_messages_view', CHAT_ID=CHAT_ID)
        else:
            return redirect('dashboard:employer_messages_view', CHAT_ID=CHAT_ID)
