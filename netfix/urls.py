from django.contrib import admin
from django.urls import include, path
from services.views import mark_service_complete, submit_review
from . import views as v

# Main URL patterns for the netfix project
urlpatterns = [
    # Django admin interface
    path("admin/", admin.site.urls),

    # Main app URLs
    path("", include("main.urls")),

    # Service-related URLs
    path("services/", include("services.urls")),

    # User registration and authentication
    path("register/", include("users.urls")),

    # User profile URLs
    path("customer/<str:name>", v.customer_profile, name="customer_profile"),
    path("company/<str:name>", v.company_profile, name="company_profile"),

    # Service review and completion endpoints
    path(
        "submit-review/<int:service_id>/",
        submit_review,
        name="submit-review"
    ),
    path(
        "mark-service-complete/<int:service_id>/",
        mark_service_complete,
        name="mark-service-complete"
    ),
]
