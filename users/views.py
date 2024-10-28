from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.urls import reverse
from django.views.generic import CreateView, TemplateView
from django.contrib.auth import get_user_model
from .forms import CompanyRegistrationForm, CustomerRegistrationForm, UserLoginForm
from .models import Company, Customer, User

User = get_user_model()  # Get the custom User model


def login_view(request):
    """
    Handle user login for both company and customer users.
    Validates credentials and redirects to appropriate profile page.
    """
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            # Extract form data
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email") 
            password = form.cleaned_data["password"]
            user_type = form.cleaned_data["user_type"]

            # Get user by email if provided, otherwise by username
            try:
                user = User.objects.get(email=email) if email else User.objects.get(username=username)
            except User.DoesNotExist:
                messages.error(request, "User not found.")
                return render(request, "login.html", {"form": form})

            # Authenticate user credentials
            user = authenticate(request, username=user.username, password=password)
            if user:
                # Check if user type matches account type
                if (user.is_company and user_type == "company") or (user.is_customer and user_type == "customer"):
                    login(request, user)
                    # Redirect to appropriate profile page
                    profile_type = "company_profile" if user.is_company else "customer_profile"
                    return redirect(reverse(profile_type, kwargs={"name": user.username}))
                else:
                    messages.error(request, "User type mismatch.")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Please correct the errors below.")

        return render(request, "login.html", {"form": form})
    
    # GET request - display empty form
    return render(request, "login.html", {"form": UserLoginForm()})


def register_company(request):
    """
    Handle company registration.
    Creates both User and Company instances and logs in the new user.
    """
    if request.method == "POST":
        form = CompanyRegistrationForm(request.POST)
        if form.is_valid():
            # Extract form data
            cleaned_data = form.cleaned_data
            
            # Create base user account
            user = User.objects.create_user(
                username=cleaned_data["username"],
                email=cleaned_data["email"],
                password=cleaned_data["password"]
            )
            user.is_company = True
            user.save()

            # Create associated company profile
            Company.objects.create(
                user=user,
                username=cleaned_data["username"],
                email=cleaned_data["email"],
                field_of_work=cleaned_data["field_of_work"],
                description=cleaned_data.get("description", "")
            )

            # Log in and redirect
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect(reverse("company_profile", kwargs={"name": user.username}))

        messages.error(request, "Please correct the errors below.")
    else:
        form = CompanyRegistrationForm()

    return render(request, "register_company.html", {"form": form})


def choose_registration(request):
    """Display registration type selection page."""
    return render(request, "user_choice.html")


def register_customer(request):
    """
    Handle customer registration.
    Creates both User and Customer instances and logs in the new user.
    """
    if request.method == "POST":
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            # Create and save user with customer flag
            user = form.save(commit=False)
            user.is_customer = True
            user.set_password(form.cleaned_data["password"])
            user.save()

            # Create associated customer profile
            Customer.objects.create(
                user=user,
                date_of_birth=form.cleaned_data["date_of_birth"]
            )

            # Log in and redirect
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("main:home")

        messages.error(request, "Please correct the errors below.")
    else:
        form = CustomerRegistrationForm()

    return render(request, "register_customer.html", {"form": form})
