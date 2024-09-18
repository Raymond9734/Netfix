from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.db.models import Count
from users.models import Company, Customer, User
from django.contrib.auth.decorators import login_required
from .models import Service, RequestedService
from .forms import CreateNewService, RequestServiceForm
from django.core.serializers import serialize
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt


@login_required(login_url=reverse_lazy("users:choose_registration"))
def index(request, id):
    service = Service.objects.get(id=id)
    return render(request, "services/single_service.html", {"service": service})


@login_required(login_url=reverse_lazy("users:choose_registration"))
def create(request):
    # Get the current company
    company = request.user.company

    if request.method == "POST":
        # Get choices based on the company's field_of_work
        if company.field_of_work == "All in One":
            # All choices available
            choices = Service._meta.get_field("field").choices
        else:
            # Only the registered field of work is available
            choices = [(company.field_of_work, company.field_of_work)]

        form = CreateNewService(request.POST, choices=choices)
        if form.is_valid():
            # Save the new service
            Service.objects.create(
                company=company,
                name=form.cleaned_data["name"],
                description=form.cleaned_data["description"],
                price_hour=form.cleaned_data["price_hour"],
                field=form.cleaned_data["field"],
            )
            return redirect(
                reverse("company_profile", kwargs={"name": company.username})
            )
    else:
        # Set choices based on the company's field_of_work
        if company.field_of_work == "All in One":
            choices = Service._meta.get_field("field").choices
        else:
            choices = [(company.field_of_work, company.field_of_work)]

        form = CreateNewService(choices=choices)

    return render(request, "services/create_service.html", {"form": form})


@login_required(login_url=reverse_lazy("users:choose_registration"))
def request_service(request, company_name, service_id):
    company = get_object_or_404(Company, username=company_name)
    service = get_object_or_404(Service, id=service_id)

    if request.method == "POST":
        form = RequestServiceForm(request.POST)
        if form.is_valid():
            requested_service = form.save(commit=False)
            requested_service.company = company
            requested_service.service_name = service
            requested_service.service_field = service.field
            requested_service.requested_by = request.user
            requested_service.save()
            return redirect("main:home")
    else:
        form = RequestServiceForm()

    return render(
        request,
        "services/request_service.html",
        {"form": form, "company": company, "service": service},
    )


@login_required(login_url=reverse_lazy("users:choose_registration"))
def services_list(request):
    # Fetch all services from the database
    services = Service.objects.all().order_by("-date")  # Newest first by default
    return render(request, "service_main.html", {"services": services})


@login_required(login_url=reverse_lazy("users:choose_registration"))
def service_by_category(request):
    services = Service.objects.all().select_related("company")
    services_json = json.loads(serialize("json", services))

    # Extract the fields we need for services, including company data
    services_data = [
        {
            "id": service["pk"],
            "name": service["fields"]["name"],
            "description": service["fields"]["description"],
            "price_hour": str(
                service["fields"]["price_hour"]
            ),  # Convert Decimal to string
            "rating": service["fields"]["rating"],
            "field": service["fields"]["field"],
            "company": {
                "id": service["fields"]["company"],
                "username": services[
                    i
                ].company.username,  # Assuming `name` is a field in the `Company` model
            },
        }
        for i, service in enumerate(services_json)
    ]

    # Prepare categories data
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
    # Group by service_name and count how many times each service_name has been requested
    services = (
        RequestedService.objects.values(
            "service_name", "service_field", "company__username", "rating"
        )
        .annotate(request_count=Count("service_name"))
        .order_by("-request_count")[:5]
    )

    # Convert QuerySet to a list of dictionaries
    services_list = list(services)  # Convert QuerySet to a list

    # Render the template with the services data
    return render(
        request,
        "services/most_requested_services.html",
        {
            "services": services_list,  # Pass the list to the template
        },
    )


@require_POST
@login_required(login_url=reverse_lazy("users:choose_registration"))
def submit_review(request, service_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            review = data.get("review", "")
            rating = int(data.get("rating", 0))
            status = data.get("status", "in_progress")

            # Ensure that the rating is between 0 and 5
            if rating < 0 or rating > 5:
                return JsonResponse({"success": False, "message": "Invalid rating."})

            # Find the requested service
            requested_service = RequestedService.objects.get(id=service_id)

            # Update the requested service with the review and rating
            requested_service.customer_review = review
            requested_service.rating = rating
            requested_service.status = status
            requested_service.save()

            return JsonResponse({"success": True})
        except RequestedService.DoesNotExist:
            return JsonResponse({"success": False, "message": "Service not found."})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
    else:
        return JsonResponse({"success": False, "message": "Invalid request method."})


@require_POST
@login_required(login_url=reverse_lazy("users:choose_registration"))
def mark_service_complete(request, service_id):
    """
    Marks a requested service as completed.
    """
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
    # Retrieve the specific service by its ID
    service = get_object_or_404(Service, id=service_id)

    # Pass the service details to the template
    return render(request, "services/single_service.html", {"service": service})
