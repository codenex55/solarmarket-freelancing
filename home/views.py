from django.shortcuts import render
from django.views import View
from dashboard.models import Task
from django.contrib.auth.models import User
from dashboard.models import Task
from accounts.models import UserAdditionalInformation


# Create your views here.
class HomeView(View):
    def get(self, request, *args, **kwargs):
        # User.objects.all().delete()
        # print(User.objects.all().count())
        tasks = Task.objects.all().order_by("-timestamp")
        context = {
            "tasks":tasks
        }
        return render(request, "home/index-2.html", context)


class SingleTaskView(View):
    def get(self, request, ID, *args, **kwargs):
        context = {}
        try:
            task = Task.objects.get(id=ID)
            context["task"] = task
        except:
            return render(request, "home/404.html")
        return render(request, "home/single-task.html", context)

class AllTaskView(View):
    def get(self, request, *args, **kwargs):
        all_tasks = Task.objects.all().order_by("-timestamp")
        context = {
            "all_tasks":all_tasks
        }
        return render(request, "home/all-task.html", context)
    

class AllFreelancersView(View):
    def get(self, request, *args, **kwargs):
        all_freelancers = UserAdditionalInformation.objects.filter(user_type="freelancer")
        context = {"all_freelancers":all_freelancers}
        return render(request, "home/all-freelancers.html", context)