from django.shortcuts import render
from django.views import View
from dashboard.models import Task
from django.contrib.auth.models import User
from dashboard.models import Task
from accounts.models import UserAdditionalInformation, Freelancer, Employer
import requests
from django.http import JsonResponse


# Create your views here.
class HomeView(View):
    def get(self, request, *args, **kwargs):
        # -User.objects.all().delete()
        # print(User.objects.all().count())
        tasks = Task.objects.all().order_by("-timestamp")[:5]
        all_states = requests.get("https://nga-states-lga.onrender.com/fetch").json()
        context = {
            "tasks":tasks,
            "all_states":all_states
        }
        return render(request, "home/index-2.html", context)
    

class GetLGAView(View):
    def post(self, request, *args, **kwargs):
        state = request.POST.get("state")
        all_lga = requests.get(f"https://nga-states-lga.onrender.com/?state={state}").json()
        data = {
            "all_lga":all_lga
        }
        return JsonResponse(data)


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
    

class FreelancerProfileView(View):
    def get(self, request, ID, *args, **kwargs):
        context = {}
        try:
            freelancer = Freelancer.objects.get(id=ID)
            context["freelancer"] = freelancer
        except:
            return render(request, "home/404.html")
        return render(request, "home/freelancer-profile.html", context)
    

class AllFreelancersView(View):
    def get(self, request, *args, **kwargs):
        all_freelancers = UserAdditionalInformation.objects.filter(user_type="freelancer")
        context = {"all_freelancers":all_freelancers}
        return render(request, "home/all-freelancers.html", context)
    

class FreelancerSearchView(View):
    def post(self, request, *args, **kwargs):
        results = Freelancer.objects.all()

        all_states = requests.get("https://nga-states-lga.onrender.com/fetch").json()

        lga = request.POST.get('lga')
        state = request.POST.get('state')
        category = request.POST.get('category')
        maximum_pay = request.POST.get("maximum_pay")
        print(maximum_pay)

        filters = {
        }

        print(lga, state, category)

        if lga:
            filters['lga'] = lga
        if state:
            filters['state'] = state
        if category:
            filters['speciality'] = category
        if maximum_pay:
            filters['minimum_pay__lte'] = float(maximum_pay)

        results = results.filter(**filters)

        print(results)

        context = {
            'results': results,
            "all_states": all_states,
            "state":state,
            "lga":lga,
            "category":category,
            "maximum_pay":maximum_pay
        }

        if state:
            all_lgas = requests.get(f"https://nga-states-lga.onrender.com/?state={state}").json()
            context["all_lgas"] = all_lgas

        return render(request, 'home/freelancer_search_results.html', context)


# nationality = models.CharField(max_length=100, default="Nigeria")
#     speciality = models.CharField(max_length=100, choices=SPECIALITY, null=True, blank=True)
#     state = models.CharField(max_length=100, null=True, blank=True)
#     lga = models.CharField(max_length=100, null=True, blank=True)
#     tagline = models.CharField(max_length=250, null=True, blank=True)
#     self_introduction = models.TextField(null=True, blank=True)
#     minimum_pay = models.FloatField(null=True, blank=True)