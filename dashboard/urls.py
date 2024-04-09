from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    # EMPLOYER DASHBOARD
    path("employer-dashboard/", views.EmployerDashBoardHome.as_view(), name="employer_dashboard_home_view"),
    path("employer-post-a-task/", views.EmployerPostTask.as_view(), name="employer_post_task_view"),
    path("employer-manage-task/", views.EmployerManageTask.as_view(), name="employer_manage_task_view"),
    path("employer-bookmarks/", views.EmployerBookmark.as_view(), name="employer_bookmarks_view"),
    path("employer-reviews/", views.EmployerReview.as_view(), name="employer_reviews_view"),
    path("employer-settings/", views.EmployerSettings.as_view(), name="employer_settings_view"),


    # FREELANCER DASHBOARD
    path("freelancer-dashboard/", views.FreelancerDashBoardHome.as_view(), name="freelancer_dashboard_home_view"),
    path("freelancer-bookmarks/", views.FreelancerBookmark.as_view(), name="freelancer_bookmarks_view"),
    path("freelancer-reviews/", views.FreelancerReview.as_view(), name="freelancer_reviews_view"),
    path("freelancer-settings/", views.FreelancerSettings.as_view(), name="freelancer_settings_view"),
]