from django.urls import path
from django.contrib.auth import views
from django.contrib.auth.views import LoginView

from .forms import UserLoginForm
from . import views as v

app_name = "users"

urlpatterns = [
    path("company_registration/", v.register_company, name="register_company"),
    path("customer_registration/", v.register_customer, name="register_customer"),
    # path("login/", v.LoginUserView, name="login_user"),
    # path('cpmpany_profile',v.)
    path("login/", v.login_view, name="login"),
    path("chooseregistration/", v.choose_registration, name="choose_registration"),
]
