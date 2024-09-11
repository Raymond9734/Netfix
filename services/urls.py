from django.urls import path
from . import views as v


app_name = "services"
urlpatterns = [
    path("", v.service_list, name="services_list"),
    path("create/", v.create, name="services_create"),
    path("<int:id>", v.index, name="index"),
    path(
        "request_service/<slug:company_name>/<int:service_id>/",
        v.request_service,
        name="request_service",
    ),
    path("<slug:field>/", v.service_field, name="services_field"),
]
