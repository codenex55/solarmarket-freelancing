from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import UserAdditionalInformation
from django.db import transaction  # Import transaction module


# Create your views here.


class SignUpView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "accounts/register.html")
    
    def post(self, request, *args, **kwargs):
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        user_type = request.POST.get("user_type")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        print(first_name)
        print(last_name)
        print(user_type)
        print(email)
        print(password1)
        print(password2)

        if User.objects.filter(username=email).exists():
            messages.error(request, "An account with that email already exist")
            return redirect ("accounts:signup_view")
        else:
            if password1 == password2:
                if len(password1) > 7:
                    l, u, s, d = 0, 0, 0, 0
                    for i in password1:
                        if (i.islower()):
                            l += 1
                        if (i.isupper()):
                            u += 1
                        if (i.isdigit()):
                            d += 1
                        if (i=="~" or i=="`" or i=="!" or i=="@" or i=="#" or i=="$" or i=="%" or i=="^" or i=="&" or i=="*" or i=="(" or i==")" or i=="-" or i=="_" or i=="+" or i=="=" or i=="{" or i=="}" or i=="[" or i=="]" or i=="|" or i=="\\" or i=="<" or i==">" or i=="?" or i=="/"):
                            s += 1
                    if (l>=1 and u>=1 and s>=1 and d>=1 and l+s+u+d==len(password1)):

                        user = User.objects.create_user(username=email, email=email, password=password1, first_name=first_name, last_name=last_name)

                        # Set account as inactive until verified
                        user.is_active = False
                        user.save()

                        user_info = UserAdditionalInformation.objects.get(user=user)
                        user_info.user_type = user_type
                        user_info.save()

                        # print(user_info.user_type)

                        # Generate verification token
                        token_generator = default_token_generator
                        uid = urlsafe_base64_encode(force_bytes(user.pk))
                        token = token_generator.make_token(user)
                        
                        # Build verification URL
                        current_site = get_current_site(request)
                        verification_url = reverse("accounts:verify_email_view", kwargs={'uidb64': uid, 'token': token})
                        verification_link = ""
                        if settings.DEBUG == True:
                            verification_link = f"http://{current_site.domain}{verification_url}"
                        else:
                            verification_link = f"https://{current_site.domain}{verification_url}"
                        
                        # Send verification email
                        context = {
                            "verification_link":verification_link
                        }
                        html_message = render_to_string("accounts/email-code-sending.html", context=context)
                        plain_message = strip_tags(html_message)
                        message = EmailMultiAlternatives(
                            subject = 'SolarMarketHub | Confirm Email Address',
                            body = plain_message,
                            from_email = settings.EMAIL_HOST_USER,
                            to = [email, ]
                        )
                        message.attach_alternative(html_message, "text/html")
                        message.send()
                        
                        return redirect("accounts:email_verification_view")

                    else:
                        messages.error(request, "Password must contain atleast 1 Uppercase, 1 lowercase, 1 digit and a special character and at least 8 characters long")
                        return redirect ("accounts:signup_view")
                else:
                    messages.error(request, "Password too short. Your password must contain at least 8 characters.")
                    return redirect ("accounts:signup_view")
            else:
                messages.error(request, "Password mismatch")
                return redirect ("accounts:signup_view")
            

class EmailVerificationView(View):
    def get(self, request):
        return render(request, "accounts/verification-email.html")


class VerifyEmailView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
            user_info = UserAdditionalInformation.objects.get(user=user)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()

            user_info.is_verified = True
            user_info.save()
            messages.success(request, "Your email has been verified. You can now log in.")
            return redirect("accounts:login_view")
        else:
            messages.error(request, "Invalid verification link.")
            return redirect("accounts:login_view")
        

class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "accounts/login.html")
    
    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        password = request.POST.get("password")
        print(email)
        print(password)
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            if user.is_active:
                # Check if the user's account is verified
                try:
                    additional_info = UserAdditionalInformation.objects.get(user=user)
                    if additional_info.is_verified:
                        login(request, user)
                        print(additional_info.user_type)
                        if additional_info.user_type == "freelancer":
                            return redirect("dashboard:freelancer_dashboard_home_view")  # Redirect to freelancer dashboard after login
                        elif additional_info.user_type == "employer":
                            return redirect("dashboard:employer_dashboard_home_view")  # Redirect to employer dashboard after login
                        else:
                            print("here7")
                    else:
                        messages.error(request, "Your account is not verified. Please check your email for the verification link.")
                        return redirect("accounts:login_view")
                except UserAdditionalInformation.DoesNotExist:
                    messages.error(request, "Additional information for this user does not exist.")
                    return redirect("accounts:login_view")
            else:
                messages.error(request, "Your account is not verified.")
                return redirect("accounts:login_view")
        else:
            messages.error(request, "Invalid email or password.")
            return redirect("accounts:login_view")
