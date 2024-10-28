from django.urls import path
from . import views as v


app_name = "services"
urlpatterns = [
    # Create a new service
    path("create/", v.create, name="services_create"),

    # View details for a single service by ID
    path("<int:id>", v.index, name="index"),

    # Request a service from a specific company
    path(
        "request_service/<str:company_name>/<int:service_id>/",
        v.request_service,
        name="request_service",
    ),

    # List all services
    path("service_list/", v.services_list, name="service_list"),

    # Filter services by category
    path("service_category/", v.service_by_category, name="service_by_category"),

    # View most requested services
    path(
        "most_requested_service/",
        v.most_requested_services,
        name="most_requested_services",
    ),

    # View detailed information for a specific service
    path("service_detail/<int:service_id>/", v.service_detail, name="service_detail"),
]
