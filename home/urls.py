from django.urls import path
from . import views

app_name = "home"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home_view"),
    path("tasks/<int:ID>/", views.SingleTaskView.as_view(), name="single_task_view"),
    path("all-freelancers/", views.AllFreelancersView.as_view(), name="all_freelancers_view"),
    path("all-tasks/", views.AllTaskView.as_view(), name="all_tasks_view"),
]