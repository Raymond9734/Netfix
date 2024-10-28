from django.contrib import admin
from .models import Service, RequestedService


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """Admin configuration for Service model."""
    list_display = ("id", "name", "price_hour", "field", "date", "rating")
    list_filter = ("field",)  # Enable filtering by service field
    search_fields = ("name", "description")  # Enable search by name and description
    ordering = ("name",)  # Default ordering by name


class RequestedServiceAdmin(admin.ModelAdmin):
    """Admin configuration for RequestedService model."""
    list_display = (
        "requested_by",
        "company", 
        "service_name",
        "service_field",
        "address",
        "service_time_hours",
        "requested_at",
        "customer_review",
        "status",
        "rating",
    )
    list_filter = ("status", "company", "service_field")  # Add service_field filter
    search_fields = ("service_field", "address", "company__name", "requested_by__username")
    ordering = ("-requested_at",)  # Most recent first
    date_hierarchy = "requested_at"  # Add date-based navigation
    readonly_fields = ("requested_at",)  # Prevent editing request timestamp


admin.site.register(RequestedService, RequestedServiceAdmin)
