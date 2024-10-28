from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from users.models import User, Company, Customer
from services.models import RequestedService, Service
from decimal import Decimal, ROUND_HALF_UP
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.db.models import Prefetch


@login_required(login_url=reverse_lazy("users:choose_registration"))
def customer_profile(request, name):
    """
    Display customer profile with their service request history and calculated costs.
    
    Args:
        request: The HTTP request object
        name: Username of the customer
        
    Returns:
        Rendered customer profile template with user details and service history
    """
    # Get the User and related Customer profile in a single query
    user = get_object_or_404(User.objects.select_related('customer_profile'), username=name)
    customer = user.customer_profile

    # Get service requests with company and service info prefetched to reduce queries
    service_requests = RequestedService.objects.filter(
        requested_by=request.user
    ).select_related(
        'company'
    ).prefetch_related(
        Prefetch(
            'company__service_set',
            queryset=Service.objects.only('name', 'price_hour', 'company'),
            to_attr='services'
        )
    ).order_by("-requested_at")

    # Calculate costs and prepare data for template
    services_with_cost = []
    for request_service in service_requests:
        # Find matching service from prefetched data
        service = next(
            (s for s in request_service.company.services 
             if s.name == request_service.service_name),
            None
        )
        
        if service:
            # Calculate and round total cost
            total_cost = (service.price_hour * 
                         Decimal(request_service.service_time_hours)
                        ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            
            services_with_cost.append({
                "service_request": request_service,
                "total_cost": total_cost
            })

    # Calculate customer's current age
    today = timezone.now().date()
    age = (
        today.year
        - customer.date_of_birth.year
        - ((today.month, today.day) < 
           (customer.date_of_birth.month, customer.date_of_birth.day))
    )

    return render(
        request,
        "users/customer_profile.html",
        {
            "user": user,
            "customer": customer,
            "services_with_cost": services_with_cost,
            "age": age,
        },
    )


@login_required(login_url=reverse_lazy("users:choose_registration"))
def company_profile(request, name):
    """
    Display company profile with their services and customer reviews.
    
    Args:
        request: The HTTP request object
        name: Username of the company
        
    Returns:
        Rendered company profile template with services and reviews
    """
    # Get company user with related company profile
    user = get_object_or_404(User.objects.select_related('company_profile'), 
                            username=name)
    company = user.company_profile

    # Get company services and reviews in optimized queries
    services = Service.objects.filter(
        company=company
    ).order_by("-date")

    reviews = RequestedService.objects.filter(
        company=company
    ).select_related(
        'requested_by'
    ).order_by("-requested_at")

    return render(
        request,
        "users/profile.html",
        {
            "user": user,
            "services": services,
            "reviews": reviews
        },
    )
