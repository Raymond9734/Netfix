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
    if request.user.is_authenticated:
        # Redirect the user to the homepage if they are already logged in
        return redirect("main:home")
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            # Form validation is handled in the form class itself
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data["password"]
            user_type = form.cleaned_data["user_type"]

            # Find the user by the email or username (as validated)
            user = (
                User.objects.get(email=email)
                if email
                else User.objects.get(username=username)
            )

            # Authenticate and log in the user
            user = authenticate(request, username=user.username, password=password)
            if user:
                login(request, user)
                if user.is_company and user_type == "company":
                    return redirect(
                        reverse("company_profile", kwargs={"name": user.username})
                    )
                elif user.is_customer and user_type == "customer":
                    return redirect(
                        reverse("customer_profile", kwargs={"name": user.username})
                    )
                else:
                    messages.error(request, "User type mismatch.")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            # Form errors are already handled in the form class
            messages.error(request, "Please correct the errors below.")

        # Render the form with errors
        return render(request, "login.html", {"form": form})
    else:
        form = UserLoginForm()  # Create an empty form instance
        return render(request, "login.html", {"form": form})


def register_company(request):
    if request.user.is_authenticated:
        # Redirect the user to the homepage if they are already logged in
        return redirect("main:home")
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
    if request.user.is_authenticated:
        # Redirect the user to the homepage if they are already logged in
        return redirect("main:home")
    return render(request, "user_choice.html")


def register_customer(request):
    if request.user.is_authenticated:
        # Redirect the user to the homepage if they are already logged in
        return redirect("main:home")
    if request.method == "POST":
        form = CustomerRegistrationForm(request.POST)

        if form.is_valid():
            # Save the user
            user = form.save(commit=False)
            user.is_customer = True
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
