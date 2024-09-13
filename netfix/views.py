from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from users.models import User, Company, Customer
from services.models import RequestedService, Service


def home(request):
    return render(request, "users/home.html", {"user": request.user})


def customer_profile(request, name):
    # Get the User object or return a 404 if not found
    user = get_object_or_404(User, username=name)

    # Get the Customer instance related to this User
    customer = get_object_or_404(Customer, user=user)

    # Get service requests for the logged-in user
    service_requests = RequestedService.objects.filter(requested_by=request.user)

    # Calculate the current age of the customer
    today = timezone.now().date()
    age = (
        today.year
        - customer.date_of_birth.year
        - (
            (today.month, today.day)
            < (customer.date_of_birth.month, customer.date_of_birth.day)
        )
    )

    # Render the profile template with the user, customer details, and service requests
    return render(
        request,
        "users/customer_profile.html",
        {
            "user": user,
            "customer": customer,
            "service_requests": service_requests,
            "age": age,  # Pass the age to the template
        },
    )


def company_profile(request, name):
    # fetches the company user and all of the services available by it
    user = User.objects.get(username=name)
    services = Service.objects.filter(company=Company.objects.get(user=user)).order_by(
        "-date"
    )

    return render(request, "users/profile.html", {"user": user, "services": services})
