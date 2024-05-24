from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    # EMPLOYER DASHBOARD
    path("employer-dashboard/", views.EmployerDashBoardHome.as_view(), name="employer_dashboard_home_view"),
    path("employer-post-a-task/", views.EmployerPostTask.as_view(), name="employer_post_task_view"),
    path("employer-manage-task/", views.EmployerManageTask.as_view(), name="employer_manage_task_view"),
    path("employer-manage-bidders/<int:TASK_ID>/", views.EmployerManageBidder.as_view(), name="employer_manage_bidder_view"),
    path("employer-remove-bidder/<int:BID_ID>/", views.EmployerRemoveBidder.as_view(), name="employer_remove_bidder_view"),
    path("employer-bookmarks/", views.EmployerBookmark.as_view(), name="employer_bookmarks_view"),
    path("employer-reviews/", views.EmployerReview.as_view(), name="employer_reviews_view"),
    path("employer-settings/", views.EmployerSettings.as_view(), name="employer_settings_view"),
    path("delete-task/<int:TASK_ID>/", views.DeleteTaskView.as_view(), name="delete_task_view"),
    path("employer-payment-successful/", views.EmployerPaymentSuccess.as_view(), name="employer_payment_success_view"),


    # FREELANCER DASHBOARD
    path("freelancer-dashboard/", views.FreelancerDashBoardHome.as_view(), name="freelancer_dashboard_home_view"),
    path("freelancer-bookmarks/", views.FreelancerBookmark.as_view(), name="freelancer_bookmarks_view"),
    path("freelancer-reviews/", views.FreelancerReview.as_view(), name="freelancer_reviews_view"),
    path("freelancer-settings/", views.FreelancerSettings.as_view(), name="freelancer_settings_view"),
    path("freelancer-active-bids/", views.FreelancerActiveBids.as_view(), name="freelancer_active_bids_view"),
    path("delete-bid/<int:BID_ID>/", views.DeleteBidView.as_view(), name="delete_bid_view"),


    # CHAT SYSTEM
    path("freelancer-messages/<int:CHAT_ID>", views.FreelancerMessages.as_view(), name="freelancer_messages_view"),
    path("employer-messages/<int:CHAT_ID>", views.EmployerMessages.as_view(), name="employer_messages_view"),
    path("initiate-chat/<int:RECIPIENT_ID>/", views.InitiateChatView.as_view(), name="initiate_chat_view"),
    path("send-message/<int:CHAT_ID>/", views.SendMessage.as_view(), name="send_message_view"),


    # VERIFY PAYMENT
    path("verify-payment/", views.VerifyPaymentView.as_view(), name="verify_payment_view"),
]

