from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup_view'),
    path('login/', views.LoginView.as_view(), name='login_view'),
    path('logout/', views.LogoutView.as_view(), name='logout_view'),
    path('email-verification/', views.EmailVerificationView.as_view(), name='email_verification_view'),
    path('verify-email/<uidb64>/<token>/', views.VerifyEmailView.as_view(), name='verify_email_view'),  # URL for email verification
]