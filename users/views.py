from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.urls import reverse
from django.views.generic import CreateView, TemplateView
from django.contrib.auth import get_user_model
from .forms import (
    CompanyRegistrationForm,
    CustomerRegistrationForm,
)
from .models import Company, Customer, User

User = get_user_model()  # Get the custom User model


def register(request):
    return render(request, "users/register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        user_type = request.POST.get("user_type")

        # Check if the user exists and authenticate
        try:
            user = User.objects.get(username=username, email=email)
        except User.DoesNotExist:
            messages.error(request, "Invalid username or email.")
            return render(request, "login.html")

        # Authenticate the user
        user = authenticate(username=username, password=password)
        if user is not None:
            # Check if the user_type matches the registered user type
            if user.is_company and user_type == "company":
                login(request, user)
                return redirect(reverse(
                    "company_profile", kwargs={"name": username})
                )  # Redirect to company profile
            elif user.is_customer and user_type == "customer":
                login(request, user)
                return redirect("customer_profile")  # Redirect to customer profile
            else:
                messages.error(request, "User type mismatch.")
                return render(request, "login.html")

        # If authentication fails
        messages.error(request, "Invalid username or password.")
        return render(request, "login.html")

    # If not POST, render the login page
    return render(request, "login.html")


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
