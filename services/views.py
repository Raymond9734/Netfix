from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from users.models import Company, Customer, User
from django.contrib.auth.decorators import login_required
from .models import Service
from .forms import CreateNewService, RequestServiceForm


@login_required
def index(request, id):
    service = Service.objects.get(id=id)
    return render(request, "services/single_service.html", {"service": service})


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


def service_field(request, field):
    # search for the service present in the url
    field = field.replace("-", " ").title()
    services = Service.objects.filter(field=field)
    return render(
        request, "services/field.html", {"services": services, "field": field}
    )


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


def services_list(request):
    # Fetch all services from the database
    services = Service.objects.all().order_by("-date")  # Newest first by default
    return render(request, "service_main.html", {"services": services})
