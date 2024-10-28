from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.db.models import Count
from users.models import Company
from django.contrib.auth.decorators import login_required
from .models import Service, RequestedService
from .forms import CreateNewService, RequestServiceForm
from django.core.serializers import serialize
import json
from django.http import HttpResponseForbidden, JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages


@login_required(login_url=reverse_lazy("users:choose_registration"))
def index(request, id):
    """Display details for a single service"""
    service = get_object_or_404(Service, id=id)
    return render(request, "services/single_service.html", {"service": service})


@login_required(login_url=reverse_lazy("users:choose_registration"))
def create(request):
    """
    Create a new service for a company.
    Handles both GET and POST requests.
    """
    # Check if user is logged in, is a company and matches username
    if (
        not request.user.is_authenticated
        or not request.user.is_company
        or request.user.username != request.user.username
    ):
        return render(request, "403.html", status=403)

    try:
        company = Company.objects.get(user=request.user)
    except Company.DoesNotExist:
        messages.error(request, "Company profile not found.")
        return redirect("main:home")

    # Determine service field choices based on company's field of work
    choices = (
        Service._meta.get_field("field").choices
        if company.field_of_work == "All in One"
        else [(company.field_of_work, company.field_of_work)]
    )

    if request.method == "POST":
        form = CreateNewService(request.POST, choices=choices)
        if form.is_valid():
            name = form.cleaned_data["name"]

            # Prevent duplicate service names for same company
            if Service.objects.filter(company=company, name=name).exists():
                form.add_error(
                    "name",
                    "The service name you entered already exists for your company.",
                )
            else:
                Service.objects.create(
                    company=company,
                    name=name,
                    description=form.cleaned_data["description"],
                    price_hour=form.cleaned_data["price_hour"],
                    field=form.cleaned_data["field"],
                )
                return redirect(
                    reverse("company_profile", kwargs={"name": company.username})
                )
    else:
        form = CreateNewService(choices=choices)

    return render(request, "services/create_service.html", {"form": form})


@login_required(login_url=reverse_lazy("users:choose_registration"))
def request_service(request, company_name, service_id):
    """Handle service request creation for a specific service"""
    # Check if user is logged in and is a customer
    if not request.user.is_authenticated or not request.user.is_customer:
        return render(request, "403.html", status=403)

    company = get_object_or_404(Company, username=company_name)
    service = get_object_or_404(Service, id=service_id)

    if request.method == "POST":
        form = RequestServiceForm(request.POST)
        if form.is_valid():
            # Verify username matches logged in user
            if request.user.username != request.user.username:
                return render(request, "403.html", status=403)

            requested_service = form.save(commit=False)
            requested_service.company = company
            requested_service.service_name = service
            requested_service.service_field = service.field
            requested_service.requested_by = request.user
            requested_service.save()
            return redirect(
                reverse("customer_profile", kwargs={"name": request.user.username})
            )
    else:
        form = RequestServiceForm()

    context = {"form": form, "company": company, "service": service}
    return render(request, "services/request_service.html", context)


@login_required(login_url=reverse_lazy("users:choose_registration"))
def services_list(request):
    """Display all services ordered by date"""
    services = Service.objects.all().order_by("-date")
    return render(request, "service_main.html", {"services": services})


@login_required(login_url=reverse_lazy("users:choose_registration"))
def service_by_category(request):
    """
    Display services grouped by category with company information.
    Optimized to use select_related for company data.
    """
    services = Service.objects.all().select_related("company")
    services_json = json.loads(serialize("json", services))

    # Transform services data for template
    services_data = [
        {
            "id": service["pk"],
            "name": service["fields"]["name"],
            "description": service["fields"]["description"],
            "price_hour": str(service["fields"]["price_hour"]),
            "rating": service["fields"]["rating"],
            "field": service["fields"]["field"],
            "company": {
                "id": service["fields"]["company"],
                "username": services[i].company.username,
            },
        }
        for i, service in enumerate(services_json)
    ]

    categories_data = [
        {"id": choice[0], "name": choice[1]} for choice in Service.choices
    ]

    context = {
        "services": services_data,
        "categories": categories_data,
    }
    return render(request, "services/service_by_category.html", context)


@login_required(login_url=reverse_lazy("users:choose_registration"))
def most_requested_services(request):
    """Get top 5 most requested services with request counts"""
    services = (
        RequestedService.objects.values("service_name")
        .annotate(request_count=Count("id"))
        .order_by("-request_count")[:5]
    )
    return render(
        request,
        "services/most_requested_services.html",
        {"services": list(services)},
    )


@require_POST
@login_required(login_url=reverse_lazy("users:choose_registration"))
@require_POST
@login_required(login_url=reverse_lazy("users:choose_registration"))
def submit_review(request, service_id):
    """
    Handle submission of service reviews.
    Validates rating and updates service status.
    Only allows logged in customers who requested the service.
    """
    if not request.user.is_customer:
        return HttpResponseForbidden("Only customers can submit reviews")

    try:
        data = json.loads(request.body)
        review = data.get("review", "")
        rating = int(data.get("rating", 0))
        status = data.get("status", "in_progress")

        if not 0 <= rating <= 5:
            return JsonResponse({"success": False, "message": "Invalid rating."})

        requested_service = get_object_or_404(
            RequestedService, id=service_id, requested_by=request.user
        )
        requested_service.customer_review = review
        requested_service.rating = rating
        requested_service.status = status
        requested_service.save()

        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)})


@require_POST
@login_required(login_url=reverse_lazy("users:choose_registration"))
def mark_service_complete(request, service_id):
    """Mark a requested service as completed if not already done"""
    if not request.user.is_customer:
        return HttpResponseForbidden("Only customers can mark services as complete")

    service = get_object_or_404(
        RequestedService, id=service_id, requested_by=request.user
    )

    if service.status == "completed":
        return JsonResponse(
            {"success": False, "error": "Service is already completed."}
        )

    service.status = "completed"
    service.save()
    return JsonResponse({"success": True})


@login_required(login_url=reverse_lazy("users:choose_registration"))
def service_detail(request, service_id):
    """Display detailed view of a specific service"""
    service = get_object_or_404(Service, id=service_id)
    return render(request, "services/single_service.html", {"service": service})
