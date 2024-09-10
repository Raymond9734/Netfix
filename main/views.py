from django.shortcuts import render
from django.contrib.auth import logout as django_logout

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from services.models import Service


@login_required
def home(request):
    # Query the Service model to get all services
    services = Service.objects.all()

    # You might want to query the most requested services separately
    # For demonstration, we'll assume you want to show all services as most requested services
    most_requested_services = services

    # Pass services and most_requested_services to the template context
    context = {"services": services, "most_requested_services": most_requested_services}

    return render(request, "main/home.html", context)


def logout(request):
    django_logout(request)
    return render(request, "main/logout.html")
