from django.urls import path
from django.contrib.auth import views
from django.contrib.auth.views import LoginView

from .forms import UserLoginForm
from . import views as v

# Namespace for URL patterns
app_name = "users"

urlpatterns = [
    # URL pattern for company registration page
    path("company_registration/", v.register_company, name="register_company"),
    
    # URL pattern for customer registration page 
    path("customer_registration/", v.register_customer, name="register_customer"),

    # URL pattern for login page
    path("login/", v.login_view, name="login"),
    
    # URL pattern for registration type selection page
    path("chooseregistration/", v.choose_registration, name="choose_registration"),
]
