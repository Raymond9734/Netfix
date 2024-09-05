from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views.generic import CreateView, TemplateView

from .forms import (
    CompanyRegistrationForm,
    CustomerRegistrationForm,
)
from .models import Company, Customer


def register(request):
    return render(request, "users/register.html")


def LoginUserView(request):
    pass


def register_company(request):
    if request.method == "POST":
        form = CompanyRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_company = True
            user.set_password(form.cleaned_data["password"])
            user.save()
            Company.objects.create(
                user=user,
                username=user.username,  # Or some other field value
                email=user.email,
                field_of_work=form.cleaned_data["field_of_work"],
            )
            login(request, user)  # Automatically log in the user after registration
            messages.success(request, "Registration successful.")
            return redirect("main:home")
    else:
        form = CompanyRegistrationForm()

    return render(request, "register_company.html", {"form": form})


def choose_registration(request):
    return render(request, "user_choice.html")


def register_customer(request):
    if request.method == "POST":
        form = CustomerRegistrationForm(request.POST)

        if form.is_valid():
            # Save the user
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            # Save the customer data
            customer = Customer(
                user=user, date_of_birth=form.cleaned_data["date_of_birth"]
            )
            customer.save()

            # Log in the user
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("main:home")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomerRegistrationForm()

    return render(request, "register_customer.html", {"form": form})
