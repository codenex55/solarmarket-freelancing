from django.shortcuts import render, redirect
from django.views import View
from dashboard.models import Task
from django.contrib.auth.models import User
from dashboard.models import Task, TaskBid, FreelancerReview, EmployerNotification, FreelancerNotification
from accounts.models import UserAdditionalInformation, Freelancer, Employer
import requests
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count


# Create your views here.
class HomeView(View):
    def get(self, request, *args, **kwargs):
        # -User.objects.all().delete()
        # print(User.objects.all().count())
        tasks = Task.objects.all().order_by("-timestamp")[:5]
        all_states = requests.get("https://nga-states-lga.onrender.com/fetch").json()

        solar_installation_count = Task.objects.filter(task_category='Solar Installation').count()
        solar_maintenance_count = Task.objects.filter(task_category='Solar Maintenance').count()
        ctvv_installation_count = Task.objects.filter(task_category='CCTV Installation').count()
        ctvv_maintenance_count = Task.objects.filter(task_category='CCTV Maintenance').count()

        context = {
            "tasks":tasks,
            "all_states":all_states,
            "solar_installation_count":solar_installation_count,
            "solar_maintenance_count":solar_maintenance_count,
            "ctvv_installation_count":ctvv_installation_count,
            "ctvv_maintenance_count":ctvv_maintenance_count,
        }

        if request.user.is_authenticated:
            if request.user.useradditionalinformation.user_type == "employer":
                # All Notification
                all_notification = EmployerNotification.objects.filter(read=False).exclude(notification_category="message").order_by("-timestamp")

                # notification count
                notification_count = EmployerNotification.objects.filter(read=False).exclude(notification_category="message").order_by("-timestamp").count()

                # All Message Notification
                all_message_notification = EmployerNotification.objects.filter(read=False, notification_category="message").order_by("-timestamp")

                # message notification count
                message_notification_count = EmployerNotification.objects.filter(read=False, notification_category="message").order_by("-timestamp").count()
            elif request.user.useradditionalinformation.user_type == "freelancer":
                # All Notification
                all_notification = FreelancerNotification.objects.filter(read=False).exclude(notification_category="message").order_by("-timestamp")

                # notification count
                notification_count = FreelancerNotification.objects.filter(read=False).exclude(notification_category="message").order_by("-timestamp").count()

                # All Message Notification
                all_message_notification = FreelancerNotification.objects.filter(read=False, notification_category="message").order_by("-timestamp")

                # message notification count
                message_notification_count = FreelancerNotification.objects.filter(read=False, notification_category="message").order_by("-timestamp").count()

            context["all_notification"] = all_notification
            context["notification_count"] = notification_count
            context["all_message_notification"] = all_message_notification
            context["message_notification_count"] = message_notification_count

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

        if request.user.is_authenticated:
            if request.user.useradditionalinformation.user_type == "employer":
                # All Notification
                all_notification = EmployerNotification.objects.filter(read=False).exclude(notification_category="message").order_by("-timestamp")

                # notification count
                notification_count = EmployerNotification.objects.filter(read=False).exclude(notification_category="message").order_by("-timestamp").count()

                # All Message Notification
                all_message_notification = EmployerNotification.objects.filter(read=False, notification_category="message").order_by("-timestamp")

                # message notification count
                message_notification_count = EmployerNotification.objects.filter(read=False, notification_category="message").order_by("-timestamp").count()
            elif request.user.useradditionalinformation.user_type == "freelancer":
                # All Notification
                all_notification = FreelancerNotification.objects.filter(read=False).exclude(notification_category="message").order_by("-timestamp")

                # notification count
                notification_count = FreelancerNotification.objects.filter(read=False).exclude(notification_category="message").order_by("-timestamp").count()

                # All Message Notification
                all_message_notification = FreelancerNotification.objects.filter(read=False, notification_category="message").order_by("-timestamp")

                # message notification count
                message_notification_count = FreelancerNotification.objects.filter(read=False, notification_category="message").order_by("-timestamp").count()

            context["all_notification"] = all_notification
            context["notification_count"] = notification_count
            context["all_message_notification"] = all_message_notification
            context["message_notification_count"] = message_notification_count


        try:
            task = Task.objects.get(id=ID)
            bidders = TaskBid.objects.filter(task=task).order_by("-timestamp")
            remaining_time = task.task_deadline - timezone.now()
            context["task"] = task
            context["bidders"] = bidders
            if remaining_time.days > 0:
                context["remaining_time"] = f"{remaining_time.days} days, {remaining_time.seconds // 3600} hours left"
            elif remaining_time.seconds >= 3600:
                context["remaining_time"] = f"{remaining_time.seconds // 3600} hours left"
            elif remaining_time.seconds > 0:
                context["remaining_time"] = f"{remaining_time.seconds // 60} minutes left"
            else:
                context["remaining_time"] = "Expired"
        except Task.DoesNotExist:
            return render(request, "home/404.html")
        
        return render(request, "home/single-task.html", context)

class AllTaskView(View):
    def get(self, request, *args, **kwargs):
        all_tasks = Task.objects.all().order_by("-timestamp")
        all_states = requests.get("https://nga-states-lga.onrender.com/fetch").json()
        context = {
            "all_tasks":all_tasks,
            "all_states":all_states,
        }

        if request.user.is_authenticated:
            if request.user.useradditionalinformation.user_type == "employer":
                # All Notification
                all_notification = EmployerNotification.objects.filter(read=False).exclude(notification_category="message").order_by("-timestamp")

                # notification count
                notification_count = EmployerNotification.objects.filter(read=False).exclude(notification_category="message").order_by("-timestamp").count()

                # All Message Notification
                all_message_notification = EmployerNotification.objects.filter(read=False, notification_category="message").order_by("-timestamp")

                # message notification count
                message_notification_count = EmployerNotification.objects.filter(read=False, notification_category="message").order_by("-timestamp").count()
            elif request.user.useradditionalinformation.user_type == "freelancer":
                # All Notification
                all_notification = FreelancerNotification.objects.filter(read=False).exclude(notification_category="message").order_by("-timestamp")

                # notification count
                notification_count = FreelancerNotification.objects.filter(read=False).exclude(notification_category="message").order_by("-timestamp").count()

                # All Message Notification
                all_message_notification = FreelancerNotification.objects.filter(read=False, notification_category="message").order_by("-timestamp")

                # message notification count
                message_notification_count = FreelancerNotification.objects.filter(read=False, notification_category="message").order_by("-timestamp").count()

            context["all_notification"] = all_notification
            context["notification_count"] = notification_count
            context["all_message_notification"] = all_message_notification
            context["message_notification_count"] = message_notification_count

        return render(request, "home/all-task.html", context)
    

class TaskSearchView(View):
    def get(self, request, *args, **kwargs):
        results = Task.objects.all()

        all_states = requests.get("https://nga-states-lga.onrender.com/fetch").json()

        popular_category = request.GET.get("popular_category")

        filters = {
        }

        if popular_category:
            filters['task_category'] = popular_category

        results = results.filter(**filters)

        context = {
            'results': results,
            "all_states": all_states,
        }

        if request.user.is_authenticated:
            if request.user.useradditionalinformation.user_type == "employer":
                # All Notification
                all_notification = EmployerNotification.objects.filter(read=False).exclude(notification_category="message").order_by("-timestamp")

                # notification count
                notification_count = EmployerNotification.objects.filter(read=False).exclude(notification_category="message").order_by("-timestamp").count()

                # All Message Notification
                all_message_notification = EmployerNotification.objects.filter(read=False, notification_category="message").order_by("-timestamp")

                # message notification count
                message_notification_count = EmployerNotification.objects.filter(read=False, notification_category="message").order_by("-timestamp").count()
            elif request.user.useradditionalinformation.user_type == "freelancer":
                # All Notification
                all_notification = FreelancerNotification.objects.filter(read=False).exclude(notification_category="message").order_by("-timestamp")

                # notification count
                notification_count = FreelancerNotification.objects.filter(read=False).exclude(notification_category="message").order_by("-timestamp").count()

                # All Message Notification
                all_message_notification = FreelancerNotification.objects.filter(read=False, notification_category="message").order_by("-timestamp")

                # message notification count
                message_notification_count = FreelancerNotification.objects.filter(read=False, notification_category="message").order_by("-timestamp").count()
                
            context["all_notification"] = all_notification
            context["notification_count"] = notification_count
            context["all_message_notification"] = all_message_notification
            context["message_notification_count"] = message_notification_count

        return render(request, 'home/task_search_results.html', context)


    def post(self, request, *args, **kwargs):
        results = Task.objects.all()

        all_states = requests.get("https://nga-states-lga.onrender.com/fetch").json()

        lga = request.POST.get('lga')
        state = request.POST.get('state')
        category = request.POST.get('category')
        maximum_pay = request.POST.get("maximum_pay")
        task_type = request.POST.get("task_type")

        filters = {
        }

        print(lga, state, category)

        if lga:
            filters['task_lga'] = lga
        if state:
            filters['task_state'] = state
        if category:
            filters['task_category'] = category
        if maximum_pay:
            filters['task_min_pay__lte'] = float(maximum_pay)
        if task_type:
            filters['task_type'] = task_type

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

        return render(request, 'home/task_search_results.html', context)

    

class FreelancerProfileView(View):
    def get(self, request, ID, *args, **kwargs):
        context = {}
        try:
            freelancer = Freelancer.objects.get(id=ID)
            context["freelancer"] = freelancer
        except:
            return render(request, "home/404.html")
        
        total_tasks_done = freelancer.total_tasks_done()
        context["total_tasks_done"] = total_tasks_done
        rehired_times = freelancer.rehired_times()
        context["rehired_times"] = rehired_times
        job_success = freelancer.job_success()
        context["job_success"] = job_success
        recommendation_rate = freelancer.recommendation_rate()
        context["recommendation_rate"] = recommendation_rate
        on_time_rate = freelancer.on_time_rate()
        context["on_time_rate"] = on_time_rate
        on_budget_rate = freelancer.on_budget_rate()
        context["on_budget_rate"] = on_budget_rate

        all_review = FreelancerReview.objects.filter(freelancer=freelancer).order_by("-timestamp")
        context["all_review"] = all_review

        if request.user.is_authenticated:
            if request.user.useradditionalinformation.user_type == "employer":
                # All Notification
                all_notification = EmployerNotification.objects.filter(read=False).exclude(notification_category="message").order_by("-timestamp")

                # notification count
                notification_count = EmployerNotification.objects.filter(read=False).exclude(notification_category="message").order_by("-timestamp").count()

                # All Message Notification
                all_message_notification = EmployerNotification.objects.filter(read=False, notification_category="message").order_by("-timestamp")

                # message notification count
                message_notification_count = EmployerNotification.objects.filter(read=False, notification_category="message").order_by("-timestamp").count()
            elif request.user.useradditionalinformation.user_type == "freelancer":
                # All Notification
                all_notification = FreelancerNotification.objects.filter(read=False).exclude(notification_category="message").order_by("-timestamp")

                # notification count
                notification_count = FreelancerNotification.objects.filter(read=False).exclude(notification_category="message").order_by("-timestamp").count()

                # All Message Notification
                all_message_notification = FreelancerNotification.objects.filter(read=False, notification_category="message").order_by("-timestamp")

                # message notification count
                message_notification_count = FreelancerNotification.objects.filter(read=False, notification_category="message").order_by("-timestamp").count()
                
            context["all_notification"] = all_notification
            context["notification_count"] = notification_count
            context["all_message_notification"] = all_message_notification
            context["message_notification_count"] = message_notification_count

        return render(request, "home/freelancer-profile.html", context)
    

class AllFreelancersView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.useradditionalinformation.user_type == "employer":
                # All Notification
                all_notification = EmployerNotification.objects.filter(read=False).exclude(notification_category="message").order_by("-timestamp")

                # notification count
                notification_count = EmployerNotification.objects.filter(read=False).exclude(notification_category="message").order_by("-timestamp").count()

                # All Message Notification
                all_message_notification = EmployerNotification.objects.filter(read=False, notification_category="message").order_by("-timestamp")

                # message notification count
                message_notification_count = EmployerNotification.objects.filter(read=False, notification_category="message").order_by("-timestamp").count()
            elif request.user.useradditionalinformation.user_type == "freelancer":
                # All Notification
                all_notification = FreelancerNotification.objects.filter(read=False).exclude(notification_category="message").order_by("-timestamp")

                # notification count
                notification_count = FreelancerNotification.objects.filter(read=False).exclude(notification_category="message").order_by("-timestamp").count()

                # All Message Notification
                all_message_notification = FreelancerNotification.objects.filter(read=False, notification_category="message").order_by("-timestamp")

                # message notification count
                message_notification_count = FreelancerNotification.objects.filter(read=False, notification_category="message").order_by("-timestamp").count()
        else:
            notification_count = 0
            all_message_notification = []
            message_notification_count = 0

        all_freelancers = Freelancer.objects.all()

        context = {
            "all_freelancers":all_freelancers,
            "all_notification":all_notification,
            "notification_count":notification_count,
            "all_message_notification":all_message_notification,
            "message_notification_count":message_notification_count,
        }
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



class BookmarkFreelancerView(View):
    def post(self, request, *args, **kwargs):
        freelancer_id = int(request.POST.get("freelancer_id"))
        freelancer = Freelancer.objects.get(id=freelancer_id)
        user_info = UserAdditionalInformation.objects.get(user=request.user)

        data = {}

        if request.user.useradditionalinformation.user_type == "freelancer":
            print("here")
            freelancer = Freelancer.objects.get(user_additional_info=user_info)
            if freelancer.bookmark_freelancer.filter(id=freelancer_id).exists():
                freelancer.bookmark_freelancer.remove(freelancer)
                data["message"] = "removed"
            else:
                freelancer.bookmark_freelancer.add(freelancer)
                data["message"] = "added"
        elif request.user.useradditionalinformation.user_type == "employer":
            print("here")
            employer = Employer.objects.get(user_additional_info=user_info)
            if employer.bookmark_freelancer.filter(id=freelancer_id).exists():
                employer.bookmark_freelancer.remove(freelancer)
                data["message"] = "removed"
            else:
                employer.bookmark_freelancer.add(freelancer)
                data["message"] = "added"
        return JsonResponse(data)
    

class BookmarkTaskView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        task_id = int(request.POST.get("task_id"))
        print(task_id)
        task = Task.objects.get(id=task_id)
        user_info = UserAdditionalInformation.objects.get(user=request.user)

        data = {}

        if request.user.useradditionalinformation.user_type == "freelancer":
            print("here")
            freelancer = Freelancer.objects.get(user_additional_info=user_info)
            if freelancer.bookmark_task.filter(id=task_id).exists():
                freelancer.bookmark_task.remove(task)
                data["message"] = "removed"
            else:
                freelancer.bookmark_task.add(task)
                data["message"] = "added"
        elif request.user.useradditionalinformation.user_type == "employer":
            print("here")
            employer = Employer.objects.get(user_additional_info=user_info)
            if employer.bookmark_task.filter(id=task_id).exists():
                employer.bookmark_task.remove(task)
                data["message"] = "removed"
            else:
                employer.bookmark_task.add(task)
                data["message"] = "added"

        return JsonResponse(data)
    

class BidTaskView(LoginRequiredMixin, View):
    def post(self, request, TASK_ID, *args, **kwargs):
        task = Task.objects.get(id=TASK_ID)
        user_info = UserAdditionalInformation.objects.get(user=request.user)
        freelancer = Freelancer.objects.get(user_additional_info=user_info)
        bid_amount = float(request.POST.get("bid_amount"))
        qtyInput = int(request.POST.get("qtyInput"))
        delivery_time = request.POST.get("delivery_time")

        if request.user.useradditionalinformation.user_type == "freelancer":
            if TaskBid.objects.filter(freelancer=freelancer, task=task).exists():
                bid = TaskBid.objects.get(freelancer=freelancer, task=task)
                bid.bid_amount = bid_amount
                bid.expected_delivery_time = qtyInput
                bid.expected_delivery_time_measurement = delivery_time
                bid.save()
                return redirect("dashboard:freelancer_active_bids_view")
            else:
                TaskBid.objects.create(freelancer=freelancer, task=task, bid_amount=bid_amount, expected_delivery_time=qtyInput, expected_delivery_time_measurement=delivery_time)
                return redirect("home:single_task_view", ID=TASK_ID)


