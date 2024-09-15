from django.urls import path
from . import views as v


app_name = "services"
urlpatterns = [
    path("create/", v.create, name="services_create"),
    path("<int:id>", v.index, name="index"),
    path(
        "request_service/<str:company_name>/<int:service_id>/",
        v.request_service,
        name="request_service",
    ),
    path("service_list/", v.services_list, name="service_list"),
    path("service_category/", v.service_by_category, name="service_by_category"),
    path(
        "most_requested_service/",
        v.most_requested_services,
        name="most_requested_services",
    ),
    path("service_detail/<int:service_id>/", v.service_detail, name="service_detail"),
]
