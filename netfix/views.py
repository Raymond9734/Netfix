from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from users.models import User, Company, Customer
from services.models import RequestedService, Service
from decimal import Decimal, ROUND_HALF_UP
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy


@login_required(login_url=reverse_lazy("users:choose_registration"))
def customer_profile(request, name):
    # Get the User object or return a 404 if not found
    user = get_object_or_404(User, username=name)

    # Get the Customer instance related to this User
    customer = get_object_or_404(Customer, user=user)

    # Get service requests for the logged-in user
    service_requests = RequestedService.objects.filter(requested_by=request.user)

    # Initialize a list to store service requests with calculated costs
    services_with_cost = []

    # Loop over each service request to calculate total cost
    for request_service in service_requests:
        # Get the corresponding Service object
        service = get_object_or_404(
            Service, name=request_service.service_name, company=request_service.company
        )

        # Calculate the total cost (price per hour * service time in hours)
        total_cost = service.price_hour * Decimal(request_service.service_time_hours)

        # Round the total cost to 2 decimal places
        total_cost = total_cost.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        # Append the request and its total cost to the list
        services_with_cost.append(
            {"service_request": request_service, "total_cost": total_cost}
        )

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

    # Render the profile template with the user, customer details, service requests, and total costs
    return render(
        request,
        "users/customer_profile.html",
        {
            "user": user,
            "customer": customer,
            "services_with_cost": services_with_cost,  # Pass services with cost to the template
            "age": age,  # Pass the age to the template
        },
    )


@login_required(login_url=reverse_lazy("users:choose_registration"))
def company_profile(request, name):
    # Fetch the company user
    user = get_object_or_404(User, username=name)

    # Fetch the company's services
    services = Service.objects.filter(company=Company.objects.get(user=user)).order_by(
        "-date"
    )

    # Fetch customer reviews for the company
    reviews = RequestedService.objects.filter(company__user=user).order_by(
        "-requested_at"
    )

    return render(
        request,
        "users/profile.html",
        {"user": user, "services": services, "reviews": reviews},
    )
