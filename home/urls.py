from django.urls import path
from . import views

app_name = "home"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home_view"),
    path("tasks/<int:ID>/", views.SingleTaskView.as_view(), name="single_task_view"),
    path("freelancer-profile/<int:ID>/", views.FreelancerProfileView.as_view(), name="freelancer_profile_view"),
    path("all-freelancers/", views.AllFreelancersView.as_view(), name="all_freelancers_view"),
    path("all-tasks/", views.AllTaskView.as_view(), name="all_tasks_view"),
    path("get-lga/", views.GetLGAView.as_view(), name="get_lga_view"),
    path("freelacer-search/", views.FreelancerSearchView.as_view(), name="freelancer_search_view"),
    path("task-search/", views.TaskSearchView.as_view(), name="task_search_view"),
    path("bookmark-freelancer/", views.BookmarkFreelancerView.as_view(), name="bookmark_freelancer_view"),
    path("bookmark-task/", views.BookmarkTaskView.as_view(), name="bookmark_task_view"),
    path("bid-task/<int:TASK_ID>/", views.BidTaskView.as_view(), name="bid_task_view"),
]