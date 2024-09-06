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
            # Extract cleaned data from the form
            email = form.cleaned_data["email"]
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            field_of_work = form.cleaned_data["field_of_work"]
            description = form.cleaned_data.get(
                "description", ""
            )  # Use default empty string if description is not provided

            # Create user
            user = User.objects.create_user(
                username=username, email=email, password=password
            )
            user.is_company = True
            user.save()

            # Create Company instance
            Company.objects.create(
                user=user,
                username=username,  # This assumes 'username' is a valid field in Company, adjust if needed
                email=email,
                field_of_work=field_of_work,
                description=description,
            )

            # Log in the user
            login(request, user)

            # Success message and redirect
            messages.success(request, "Registration successful.")
            return redirect(reverse("company_profile", kwargs={"name": username}))

        else:
            # Handle form errors
            messages.error(request, "Please correct the errors below.")
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
