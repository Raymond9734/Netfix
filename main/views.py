# Django imports
from django.shortcuts import render  # Remove duplicate import
from django.contrib.auth import logout as django_logout
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

# App imports
from services.models import Service


def home(request):
    """
    View function for the home page.
    Displays all services and most requested services.
    """
    # Optimize by using select_related() if Service has foreign keys
    services = Service.objects.all().select_related()

    # Could be based on number of requests or ratings
    most_requested_services = (
        Service.objects.all()
        .select_related()
    )

    context = {
        "services": services,
        "most_requested_services": most_requested_services,
    }

    return render(request, "main/home.html", context)


@login_required(login_url=reverse_lazy("users:choose_registration"))
def logout(request):
    """
    Handles user logout.
    Requires user to be logged in, redirects to registration choice if not.
    """
    django_logout(request)
    return render(request, "main/logout.html")
