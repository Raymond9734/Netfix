from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from users.models import Company, Customer

User = get_user_model()


class Service(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    description = models.TextField()
    price_hour = models.DecimalField(decimal_places=2, max_digits=100)
    rating = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)], default=0
    )
    choices = (
        ("Air Conditioner", "Air Conditioner"),
        ("Carpentry", "Carpentry"),
        ("Electricity", "Electricity"),
        ("Gardening", "Gardening"),
        ("Home Machines", "Home Machines"),
        ("House Keeping", "House Keeping"),
        ("Interior Design", "Interior Design"),
        ("Locks", "Locks"),
        ("Painting", "Painting"),
        ("Plumbing", "Plumbing"),
        ("Water Heaters", "Water Heaters"),
    )
    field = models.CharField(max_length=30, blank=False, null=False, choices=choices)
    date = models.DateTimeField(auto_now=True, null=False)

    def __str__(self):
        return self.name


class RequestedService(models.Model):
    SERVICE_STATUS_CHOICES = [
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
    ]

    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="requested_services"
    )
    service_name = models.CharField(max_length=100)
    service_field = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    service_time_hours = models.DecimalField(max_digits=5, decimal_places=2)
    requested_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=20, choices=SERVICE_STATUS_CHOICES, default="in_progress"
    )
    requested_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="requested_services"
    )  # New field to track the user who requested the service

    def __str__(self):
        return f"{self.service_field} - {self.company.username} - {self.status}"
