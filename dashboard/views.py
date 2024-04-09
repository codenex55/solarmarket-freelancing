from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import TaskCategory, Task
from django.http import JsonResponse
from django.contrib.auth.models import User
from accounts.models import UserAdditionalInformation
from django.contrib import messages

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
        all_categories = TaskCategory.objects.all().order_by("category")
        context = {
            "all_categories":all_categories
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
        return render(request, "dashboard/freelancer-settings.html")
    
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