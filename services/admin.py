from django.contrib import admin

from .models import Service,RequestedService


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price_hour", "field", "date","rating")


class RequestedServiceAdmin(admin.ModelAdmin):
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
    list_filter = ("status", "company")
    search_fields = ("service_field", "address", "company__name")
    ordering = ("-requested_at",)


admin.site.register(RequestedService, RequestedServiceAdmin)
