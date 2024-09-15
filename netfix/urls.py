from django.contrib import admin
from django.urls import include, path
from services.views import mark_service_complete, submit_review
from . import views as v

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main.urls")),
    path("services/", include("services.urls")),
    path("register/", include("users.urls")),
    path("customer/<str:name>", v.customer_profile, name="customer_profile"),
    path("company/<str:name>", v.company_profile, name="company_profile"),
    path("submit-review/<int:service_id>/", submit_review, name="submit-review"),
    path(
        "mark-service-complete/<int:service_id>/",
        mark_service_complete,
        name="mark-service-complete",
    ),
]
